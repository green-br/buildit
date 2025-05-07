import os
import math
import reframe as rfm
import reframe.utility as util
import reframe.utility.sanity as sn
from spack_base import SpackCompileOnlyBase

class SnapSpackBuild(SpackCompileOnlyBase):

    defspec = 'snap@main +openmp'
    env_spackspec = {
        'gcc-12': { 'spec': 'snap@main +openmp fflags="-fallow-argument-mismatch"' },
        'gcc-13': { 'spec': 'snap@main +openmp fflags="-fallow-argument-mismatch"' },
        'gcc-12-macs': { 'spec':'snap@main +openmp fflags="-fallow-argument-mismatch"' },
        'gcc-13-macs': { 'spec': 'snap@main +openmp fflags="-fallow-argument-mismatch"' },
    }

# RegressionTest is used so Spack uses existing environment.
# This also uses same spec.
@rfm.simple_test
class SnapSpackCheck(rfm.RegressionTest):
    
    snap_binary = fixture(SnapSpackBuild, scope='environment')
    fullspackspec = variable(str)

    descr = 'SNAP test using Spack'
    build_system = 'Spack'
    valid_systems = ['*']
    valid_prog_environs = ['*']
    

    num_nodes = parameter([1, 2, 4, 8, 16])

    num_threads = variable(int, value=2)
    exclusive_access = True
    extra_resources = {
        'memory': {'size': '0'}
    }

    #: The version of the benchmark suite to use.
    #:
    #: :type: :class:`str`
    #: :default: ``'1.0.0'``
    benchmark_version = variable(str, value='1.0.0', loggable=True)

    #: Parameter pack encoding the benchmark information.
    #:
    #: The first element of the tuple refers to the benchmark name,
    #: the second is the energy reference and the third is the
    #: tolerance threshold.
    #:
    #: :type: `Tuple[str, float, int]`
    #: :values:
    benchmark_info = parameter([
        ('qasnap', 2528),
        ('uob-hpc',  250)
    ], fmt=lambda x: x[0], loggable=True)

    executable = 'gsnap'

    keep_files = ['out']

    @run_after('init')
    def prepare_test(self):
        self.__bench, self.__ts_ref = self.benchmark_info
        self.descr = f'SNAP {self.__bench} benchmark'
        if self.__bench == 'qasnap':
            self.prerun_cmds = [
                f'curl -o inp https://raw.githubusercontent.com/lanl/SNAP/refs/heads/main/qasnap/benchmark/inp'
            ]
        else:
            self.prerun_cmds = [
                f'curl -o inp.tmp https://raw.githubusercontent.com/UoB-HPC/benchmarks/refs/heads/master/snap/benchmark.in',
                f'NY=16 NZ=16 NPEY=4 NPEZ=4 NTHREADS=2 ICHUNK=16 envsubst < inp.tmp > inp'
            ]

        self.executable_opts = ['inp', 'out']
    
    @run_after('setup')
    def set_environment(self):
        self.skip_if(
            self.num_nodes > self.current_partition.extras.get('max_nodes',128),
            'exceeded node limit'
        )
        self.build_system.environment = os.path.join(self.snap_binary.stagedir, 'rfm_spack_env')
        self.build_system.specs       = self.snap_binary.build_system.specs
        self.fullspackspec            = ' '.join(self.snap_binary.build_system.specs)
    
    @run_before('run')
    def set_job_size(self):
        proc = self.current_partition.processor
        self.use_multithreading = False
        self.num_tasks_per_node = proc.num_cores
        if self.__bench == "qasnap":
            # Approx. 1GB per MPI task. So may need underpopulate.
            if self.num_threads:
                self.num_cpus_per_task = self.num_threads
                self.num_tasks_per_node = (proc.num_cores) // self.num_threads
                self.env_vars['OMP_NUM_THREADS'] = self.num_threads
                self.env_vars['OMP_PLACES'] = 'cores'
                self.env_vars['OMP_PROC_BIND'] = 'close'


            max_tasks  = self.num_nodes * self.num_tasks_per_node
            root_tasks = (math.floor(math.sqrt(max_tasks)) // 2) * 2
            self.num_tasks = root_tasks*root_tasks
            self.num_tasks_per_node = self.num_tasks // self.num_nodes
            self.prerun_cmds.extend([
                rf"sed -i 's/nthreads=2/nthreads={self.num_threads}/' inp",
                rf"sed -i 's/npey=4/npey={root_tasks}/' inp",
                rf"sed -i 's/npez=4/npez={root_tasks}/' inp",
                rf"sed -i 's/ny=16/ny={4*root_tasks}/' inp",
                rf"sed -i 's/nz=16/nz={4*root_tasks}/' inp"
            ])
        else:
            # NG value in input limits threads.
            self.num_threads          = min(32, proc.num_cores // proc.num_sockets)
            self.num_tasks_per_socket = 1
            self.num_cpus_per_task    = self.num_threads
            self.num_tasks_per_node   = proc.num_sockets
            self.num_tasks            = self.num_nodes * self.num_tasks_per_node

            self.env_vars['OMP_NUM_THREADS'] = self.num_threads
            self.env_vars['OMP_PLACES'] = 'cores'
            self.env_vars['OMP_PROC_BIND'] = 'close'


            i=1
            yscale=1
            zscale=1
            while i < self.num_nodes:
                if yscale < zscale:
                    yscale *= 2
                else:
                    zscale *= 2
                i *= 2
            
            self.prerun_cmds.extend([
                rf"sed -i 's/nthreads=2/nthreads={self.num_threads}/' inp",
                rf"sed -i 's/npey=4/npey={self.num_tasks_per_node*yscale}/' inp",
                rf"sed -i 's/npez=4/npez={1*zscale}/' inp",
                rf"sed -i 's/ny=16/ny={self.num_tasks_per_node*12*yscale}/' inp",
                rf"sed -i 's/nz=16/nz={12*zscale}/' inp"
            ])
       
    @loggable
    @property
    def bench_name(self):
        '''The benchmark name.

        :type: :class:`str`
        '''

        return self.__bench

    @property
    def timestep_ref(self):
        '''The timestep expected to finish.

        :type: :class:`str`
        '''
        return self.__ts_ref

    @performance_function('s')
    def perf_time(self):
        return sn.extractsingle(r'Total Execution time\s+(?P<perf>\S+)',
                                'out', 'perf', float, item=-1)
    
    @performance_function('ns')
    def grind_time(self):
        return sn.extractsingle(r'Grind Time \(nanoseconds\)\s+(?P<perf>\S+)',
                                'out', 'perf', float, item=-1)

    @sanity_function
    def assert_outers(self):
        '''Assert number of outers is met'''
        outers = sn.extractsingle(r'Total inners for all time steps, outers =\s+(?P<outers>\S+)',
                                'out', 'outers', float, item=-1)
        return sn.assert_bounded(outers, 0.9*self.__ts_ref, 1.1*self.__ts_ref)

