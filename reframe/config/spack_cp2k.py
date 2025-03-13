import os
import reframe as rfm
import reframe.utility as util
import reframe.utility.sanity as sn
from spack_base import SpackCompileOnlyBase

class Cp2kSpackBuild(SpackCompileOnlyBase):
    spackspec = 'cp2k@2024.3'


# RegressionTest is used so Spack uses existing environment.
# This also uses same spec.
@rfm.simple_test
class Cp2kSpackCheck(rfm.RegressionTest):
    
    cp2k_binary = fixture(Cp2kSpackBuild, scope='environment')
    
    descr = 'Cp2k test using Spack'
    build_system = 'Spack'
    valid_systems = ['*']
    #valid_prog_environs = ['gcc-12', 'gcc-13', 'cce-17']
    valid_prog_environs = ['gcc-12']
    
    num_nodes = parameter([1, 2, 4])
    num_threads = 1
    exclusive_access = True
    extra_resources = {
        'memory': {'size': '200000'}
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
        ('H2O-64')
        #('HECBioSim/Glutamine-Binding-Protein', -724598.0, 0.001),
        #('HECBioSim/hEGFRDimer', -3.32892e+06, 0.001),
        #('HECBioSim/hEGFRDimerSmallerPL', -3.27080e+06, 0.001),
        #('HECBioSim/hEGFRDimerPair', -1.20733e+07, 0.001),
        #('HECBioSim/hEGFRtetramerPair', -2.09831e+07, 0.001)
    ], fmt=lambda x: x[0], loggable=True)

    executable = f"cp2k.psmp"

    @run_after('init')
    def prepare_test(self):
        self.__bench = self.benchmark_info
        self.descr = f'CP2K {self.__bench} benchmark'
        self.prerun_cmds = [
            f'curl -LJO https://raw.githubusercontent.com/cp2k/cp2k/refs/heads/master/benchmarks/QS/{self.__bench}.inp'
        ]
        self.executable_opts += ['-i', 'H2O-64.inp']
    
    @run_after('setup')
    def set_environment(self):
        self.build_system.environment = os.path.join(self.cp2k_binary.stagedir, 'rfm_spack_env')
        self.build_system.specs       = self.cp2k_binary.build_system.specs
    
    @run_before('run')
    def set_job_size(self):
        proc = self.current_partition.processor
        self.num_tasks_per_node = proc.num_cores
        if self.num_threads:
            self.num_tasks_per_node = (proc.num_cores) // self.num_threads
            self.env_vars['OMP_NUM_THREADS'] = self.num_threads
        self.num_tasks = self.num_tasks_per_node * self.num_nodes

    @loggable
    @property
    def bench_name(self):
        '''The benchmark name.

        :type: :class:`str`
        '''

        return self.__bench
    
    @run_before('sanity')
    def set_sanity_patterns(self):
        self.sanity_patterns = sn.assert_found(r'T I M I N G', self.stdout)

    @run_before('performance')
    def set_perf_patterns(self):
        self.perf_patterns = {
            'Maximum total time':
            sn.extractsingle(r'CP2K +([0-9]+) +([0-9.]+) +([0-9.]+) +([0-9.]+) +([0-9.]+) +([0-9.]+)', self.stdout, 6, float)
        }
