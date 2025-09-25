import os
import reframe as rfm
import reframe.utility as util
import reframe.utility.sanity as sn
import reframe.utility.osext as osext
from spack_base import SpackCompileOnlyBase

class CastepSpackBuild(SpackCompileOnlyBase):
    sourcefile = os.path.join(os.getenv('HOME'),'sources/castep/CASTEP-25.11.tar.gz')
    defspec = 'castep@25.1.1'
    env_spackspec = {
        'cce-18': { 'spec': 'castep@25.1.1', 'deps': '^cray-libsci ^cray-fftw'},
        'nvhpc-24': { 'spec': 'castep@25.1.1', 'deps': '^cray-libsci ^cray-fftw'},
    }

# RegressionTest is used so Spack uses existing environment.
# This also uses same spec.
@rfm.simple_test
class CastepSpackCheck(rfm.RegressionTest):
    
    castep_binary = fixture(CastepSpackBuild, scope='environment')
    fullspackspec = variable(str)

    descr = 'Castep test using Spack'
    build_system = 'Spack'
    valid_systems = ['*']
    valid_prog_environs = ['-no-castep']

    
    build_only = variable(int, value=0)
    num_nodes = parameter([2, 4, 8, 16, 32])
    num_threads = parameter([1,4])
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
        ('al3x3','al3x3'),
        #('DNA','polyA20-no-wat'),
        ('crambin','crambin')
    ], fmt=lambda x: x[0], loggable=True)

    executable = f"castep.mpi"


    @run_after('init')
    def prepare_test(self):
        self.__bench, self.__benchparam = self.benchmark_info
        self.descr = f'Castep {self.__bench} benchmark'
        strip_dir = 1
        if self.__bench == "al3x3":
            strip_dir = 2
        self.prerun_cmds = [
            f'cp ~/sources/castep/{self.__bench}.tgz .',
            f'tar zxvf *.tgz --strip-components {strip_dir}',
        ]
        self.postrun_cmds = [
            f'cat {self.__benchparam}.castep',
        ]
    

    @run_after('setup')
    def set_environment(self):
        self.skip_if(
            self.num_nodes > self.current_partition.extras.get('max_nodes',128),
            'exceeded node limit'
        )
        self.build_system.environment = os.path.join(self.castep_binary.stagedir, 'rfm_spack_env')
        self.build_system.specs       = self.castep_binary.build_system.specs
        self.fullspackspec            = ' '.join(self.castep_binary.build_system.specs)
    
    @run_before('run')
    def set_job_size(self):
        self.skip_if( self.build_only == 1, 'build only')

        proc = self.current_partition.processor
        self.use_multithreading = False
        self.num_tasks_per_node = proc.num_cores
        if self.num_threads:
            self.num_tasks_per_node = (proc.num_cores) // self.num_threads
            self.num_cpus_per_task = self.num_threads
            self.env_vars['OMP_NUM_THREADS'] = self.num_threads
            self.env_vars['OMP_PLACES'] = 'cores'
            self.env_vars['OMP_PROC_BIND'] = 'close'
        self.num_tasks = self.num_tasks_per_node * self.num_nodes
        self.executable_opts += [f'{self.__benchparam}']

    @loggable
    @property
    def bench_name(self):
        '''The benchmark name.

        :type: :class:`str`
        '''

        return self.__bench
    
    @sanity_function
    def parallel_efficiency(self):
        return sn.assert_found(r'Overall parallel efficiency rating', self.stdout)

    @performance_function('s')
    def total_time(self):
        return sn.extractsingle(r'Total time += +([0-9.]+) s', self.stdout, 1, float)
