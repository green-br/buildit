import os
import reframe as rfm
import reframe.utility as util
import reframe.utility.sanity as sn
from spack_base import SpackCompileOnlyBase

class NeutralSpackBuild(SpackCompileOnlyBase):

    defspec = 'neutral@master'

# RegressionTest is used so Spack uses existing environment.
# This also uses same spec.
@rfm.simple_test
class NeutralSpackCheck(rfm.RegressionTest):
    
    neutral_binary = fixture(NeutralSpackBuild, scope='environment')
    fullspackspec = variable(str)

    descr = 'Neutral test using Spack'
    build_system = 'Spack'
    valid_systems = ['*']
    valid_prog_environs = ['*']
    
    num_nodes = parameter([1])
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
        ('csp.params',)
    ], fmt=lambda x: x[0], loggable=True)

    executable = 'neutral.omp3'

    @run_after('init')
    def prepare_test(self):
        self.__bench, = self.benchmark_info
        self.descr = f'Neutral {self.__bench} benchmark'
        self.prerun_cmds = [
                f'git clone --recurse-submodules --branch=spack https://github.com/green-br/neutral.git',
                'cd neutral'
        ]
        self.executable_opts = [f'problems/{self.__bench}']
    
    @run_after('setup')
    def set_environment(self):
        self.build_system.environment = os.path.join(self.neutral_binary.stagedir, 'rfm_spack_env')
        self.build_system.specs       = self.neutral_binary.build_system.specs
        self.fullspackspec            = ' '.join(self.neutral_binary.build_system.specs)
    
    @run_before('run')
    def set_job_size(self):
        proc = self.current_partition.processor
        self.use_multithreading = False
        self.num_tasks_per_node = 1
        self.num_threads = proc.num_cores
        if self.num_threads:
            self.num_cpus_per_task  = self.num_threads
            self.num_tasks_per_node = proc.num_cores // self.num_threads
            self.env_vars['OMP_NUM_THREADS'] = self.num_threads

        self.num_tasks = self.num_nodes * self.num_tasks_per_node

    @loggable
    @property
    def bench_name(self):
        '''The benchmark name.

        :type: :class:`str`
        '''

        return self.__bench

    @performance_function('s')
    def perf(self):
        return sn.extractsingle(r'Final Wallclock\s+(?P<perf>\S+)s',
                                self.stdout, 'perf', float, item=-1)
#
#    def energy_cloverleaf(self):
#        return sn.extractsingle(fr'step:\s*{self.__ts_ref}(\s+\S+){{5}}\s+(?P<energy>\S+)',
#                                'clover.out', 'energy', float)
#
#    @performance_function('%')
#    def obtain_energy_readout(self):
#        '''Find that the obtained energy is met'''
#        ke = self.energy_cloverleaf()
#        qa_diff = 100.0*(ke/self.__nrg_ref)-100.0
#        return qa_diff
#
    @sanity_function
    def assert_complete(self):
        return sn.assert_found(r'PASSED validation', self.stdout)
