import os
import reframe as rfm
import reframe.utility as util
import reframe.utility.sanity as sn
from spack_base import SpackCompileOnlyBase

class OpenfoamSpackBuild(SpackCompileOnlyBase):
    spackspec = 'openfoam@2312'


# RegressionTest is used so Spack uses existing environment.
# This also uses same spec.
@rfm.simple_test
class OpenfoamSpackCheck(rfm.RegressionTest):

    openfoam_binary = fixture(OpenfoamSpackBuild, scope='environment')

    descr = 'Openfoam test using Spack'
    build_system = 'Spack'
    valid_systems = ['*']
    #valid_prog_environs = ['gcc-12', 'gcc-13', 'cce-17']
    valid_prog_environs = ['gcc-12']

    num_tasks = 144
    num_tasks_per_node = 144
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
    #: the second is the test data location.
    #:
    #: :type: `Tuple[str, float, float]`
    #: :values:
    benchmark_info = parameter([
        ('HPC_motorbike', 'hpc/incompressible/simpleFoam/HPC_motorbike/Large/v1912')
    ], fmt=lambda x: x[0], loggable=True)

    # Openfoam has its own launcher run in the prerun_cmds.
    executable = 'true'

    @run_after('init')
    def prepare_test(self):
        self.__bench, self.__subdir = self.benchmark_info
        self.descr = f'Openfoam {self.__bench} benchmark'
        self.prerun_cmds = [
            f'git clone https://develop.openfoam.com/committees/hpc.git',
            f'cd {self.__subdir}',
            f'sed -i "s/numberOfSubdomains.*/numberOfSubdomains {self.num_tasks};/g" system/decomposeParDict',
            f'sed -i "s/vector/normal/g" system/mirrorMeshDict',
            f'sed -i "s/^endTime.*/endTime         100;/" system/controlDict',
            f'sed -i "s/^writeInterval.*/writeInterval   1000;/" system/controlDict',
            f'curl -o system/fvSolution "https://develop.openfoam.com/Development/openfoam/-/raw/master/tutorials/incompressible/simpleFoam/motorBike/system/fvSolution?ref_type=heads"',
            f'chmod +x All*',
            f'./AllmeshL',
            f'./Allrun'
        ]

    @run_after('setup')
    def set_environment(self):
        self.build_system.environment = os.path.join(self.openfoam_binary.stagedir, 'rfm_spack_env')
        self.build_system.specs       = self.openfoam_binary.build_system.specs

    @loggable
    @property
    def bench_name(self):
        '''The benchmark name.

        :type: :class:`str`
        '''

        return self.__bench

    @performance_function('s')
    def perf(self):
        return sn.extractsingle(r'ExecutionTime =\s+(?P<perf>\S+)',
                                self.stdout, 'perf', float)

    @sanity_function
    def assert_finished(self):
        '''Assert that the job finished.'''

        return sn.all([
            sn.assert_found('Finalising parallel run', self.stdout),
        ])
  
