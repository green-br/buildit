import os
import reframe as rfm
import reframe.utility as util
import reframe.utility.sanity as sn
from spack_base import SpackCompileOnlyBase

class CloverleafRefSpackBuild(SpackCompileOnlyBase):
    spackspec = 'cloverleaf-ref@master +ieee'
    env_spackspec = {
        'gcc-12':'cloverleaf-ref@master +ieee fflags=-fallow-argument-mismatch',
        'gcc-13':'cloverleaf-ref@master +ieee fflags=-fallow-argument-mismatch',
        'gcc-13-macs':'cloverleaf-ref@master +ieee fflags=-fallow-argument-mismatch',
        'gcc-13-macs':'cloverleaf-ref@master +ieee fflags=-fallow-argument-mismatch',
    }

# RegressionTest is used so Spack uses existing environment.
# This also uses same spec.
@rfm.simple_test
class CloverleafRefSpackCheck(rfm.RegressionTest):
    
    cloverleafref_binary = fixture(CloverleafRefSpackBuild, scope='environment')
    fullspackspec = variable(str)

    descr = 'Cloverleaf-ref test using Spack'
    build_system = 'Spack'
    valid_systems = ['*']
    valid_prog_environs = ['*']
    
    num_nodes = parameter([1,2,4,8,16,32])
    num_threads = variable(int, value=1)
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
        ('clover_bm_short.in', 1.19316898756307, 87),
        ('clover_bm.in', 2.58984003503994 , 2955),
        ('clover_bm16_short.in', 0.307475452287895, 87),
        ('clover_bm16.in', 4.85350315783719, 2955)
    ], fmt=lambda x: x[0], loggable=True)

    executable = 'clover_leaf'
    keep_files = ['clover.out']

    @run_after('init')
    def prepare_test(self):
        self.__bench, self.__nrg_ref, self.__ts_ref = self.benchmark_info
        self.descr = f'Cloverleaf-ref {self.__bench} benchmark'
        self.prerun_cmds = [
            f'curl -o clover.in https://raw.githubusercontent.com/UK-MAC/CloverLeaf_ref/master/InputDecks/{self.__bench}'
        ]
    
    @run_after('setup')
    def set_environment(self):
        self.build_system.environment = os.path.join(self.cloverleafref_binary.stagedir, 'rfm_spack_env')
        self.build_system.specs       = self.cloverleafref_binary.build_system.specs
        self.fullspackspec            = ' '.join(self.cloverleafref_binary.build_system.specs)
    
    @run_before('run')
    def set_job_size(self):
        proc = self.current_partition.processor
        self.num_tasks_per_node = proc.num_cores
        if self.num_threads:
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

    @property
    def energy_ref(self):
        '''The energy reference value for this benchmark.

        :type: :class:`str`
        '''
        return self.__nrg_ref

    @property
    def timestep_ref(self):
        '''The timestep expected to finish.

        :type: :class:`str`
        '''
        return self.__ts_ref

    @performance_function('s')
    def perf(self):
        return sn.extractsingle(r'Wall clock\s+(?P<perf>\S+)',
                                'clover.out', 'perf', float, item=-1)

    def energy_cloverleaf(self):
        return sn.extractsingle(fr'step:\s*{self.__ts_ref}(\s+\S+){{5}}\s+(?P<energy>\S+)',
                                'clover.out', 'energy', float)

    @performance_function('%')
    def obtain_energy_readout(self):
        '''Find that the obtained energy is met'''
        ke = self.energy_cloverleaf()
        qa_diff = 100.0*(ke/self.__nrg_ref)-100.0
        return qa_diff

    @sanity_function
    def assert_complete(self):
        return sn.assert_found(r'Clover is finishing', 'clover.out')
