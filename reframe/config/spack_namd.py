import os
import reframe as rfm
import reframe.utility as util
import reframe.utility.sanity as sn
import reframe.utility.osext as osext
from spack_base import SpackCompileOnlyBase

class NamdSpackBuild(SpackCompileOnlyBase):
    sourcefile = os.path.join(os.getenv('HOME'),'sources/namd/NAMD_3.0_Source.tar.gz')
    defspec = 'namd@3.0'

# RegressionTest is used so Spack uses existing environment.
# This also uses same spec.
@rfm.simple_test
class NamdSpackCheck(rfm.RegressionTest):
    
    namd_binary = fixture(NamdSpackBuild, scope='environment')
    fullspackspec = variable(str)

    descr = 'NAMD test using Spack'
    build_system = 'Spack'
    valid_systems = ['*']

    valid_prog_environs = ['-no-namd']
    
    build_only = variable(int, value=0)
    num_nodes = parameter([1, 2, 4, 8, 16])
    num_percent = parameter([0,25,50,100])
    num_threads = variable(int, value=0)
    skip_large_percent = variable(int, value=0)
    exclusive_access = True
    extra_resources = {
        'memory': {'size': '0'},
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
    #: :type: `Tuple[str, float, float]`
    #: :values:
    benchmark_info = parameter([
        ('apoa1',),
        ('stmv',),
        ('stmv_nve_cuda',)
    ], fmt=lambda x: x[0], loggable=True)

    executable = f"namd3"

    @run_after('init')
    def prepare_test(self):
        self.__bench, = self.benchmark_info
        self.descr = f'NAMD {self.__bench} benchmark'
        if self.__bench == 'stmv_nve_cuda':
            self.prerun_cmds = [
                f'curl -LJO https://www.ks.uiuc.edu/Research/namd/utilities/stmv.tar.gz',
                f'curl -LJO http://www.ks.uiuc.edu/Research/namd/2.13/benchmarks/stmv_nve_cuda.namd'
            ]
        else:
            self.prerun_cmds = [
                f'curl -LJO https://www.ks.uiuc.edu/Research/namd/utilities/{self.__bench}.tar.gz',
            ]
        self.prerun_cmds.extend([
            f'curl -LJO https://www.ks.uiuc.edu/Research/namd/utilities/ns_per_day.py',
            f'chmod +x ns_per_day.py',
            f'tar zxvf *.tar.gz --strip-components 1',
            f'sed -i \'s|/usr/tmp/||\' *.namd',
            f'export SLURM_HINT=nomultithread',
            ])
        self.postrun_cmds = [
            f'cat output.txt',
            f'./ns_per_day.py output.txt'
        ]
    

    @run_after('setup')
    def set_environment(self):
        self.skip_if(
            self.num_nodes > self.current_partition.extras.get('max_nodes',128),
            'exceeded node limit'
        )
        self.skip_if(
            self.num_nodes > 1 and self.num_threads > 12,
            'different threads on single node only'
        )

        if (self.skip_large_percent == 1):
            self.skip_if(
                self.num_percent > 25,
                'issues at large thread count/percent'
            )

        self.build_system.environment = os.path.join(self.namd_binary.stagedir, 'rfm_spack_env')
        self.build_system.specs       = self.namd_binary.build_system.specs
        self.fullspackspec            = ' '.join(self.namd_binary.build_system.specs)
    
    @run_before('run')
    def set_job_size(self):
        self.skip_if( self.build_only == 1, 'build only')
        
        proc = self.current_partition.processor
        self.num_tasks_per_node = proc.num_cores // 2
        self.num_threads = 2
        self.use_multithreading = False

        if self.num_percent > 0:
            self.num_threads = int(proc.num_cores * self.num_percent ) // 100
            self.num_tasks_per_node = (proc.num_cores) // self.num_threads
            self.env_vars['OMP_NUM_THREADS'] = self.num_threads

        self.num_tasks = self.num_tasks_per_node * self.num_nodes
        if self.num_nodes == 1:
            self.extra_resources.update( {
                'network': {'type': 'single_node_vni'},
                }
            )
        self.executable_opts += [f'+setcpuaffinity +ppn {self.num_threads-1} {self.__bench}.namd > output.txt']

    @loggable
    @property
    def bench_name(self):
        '''The benchmark name.

        :type: :class:`str`
        '''

        return self.__bench
    
    @run_before('sanity')
    def set_sanity_patterns(self):
        self.sanity_patterns = sn.assert_found(r'End of program', self.stdout)

    @run_before('performance')
    def set_perf_patterns(self):
        self.perf_patterns = {
            'Nanoseconds per day:':
            sn.extractsingle(r'Nanoseconds per day: +([0-9.]+)', self.stdout, 1, float)
        }
