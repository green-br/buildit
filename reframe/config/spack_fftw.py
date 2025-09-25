import os
import reframe as rfm
import reframe.utility.sanity as sn
from spack_base import SpackCompileOnlyBase

class FftwSpackBuild(SpackCompileOnlyBase):
    executable = 'fftw-wisdom'
    defspec = 'fftw@3.3.10 cflags="-O3" cxxflags="-O3" fflags="-O3"'
    spacktest = True

@rfm.simple_test
class FftwSpackCheck(rfm.RegressionTest):
    descr = 'FFTW library check'
    build_system = 'Spack'
    valid_systems = ['*']
    valid_prog_environs = ['*']
    executable_opts = ['-V']
    fftw_binary = fixture(FftwSpackBuild, scope='environment')

    @run_after('setup')
    def set_environment(self):
        self.executable               = self.fftw_binary.executable
        self.build_system.environment = os.path.join(self.fftw_binary.stagedir, 'rfm_spack_env')
        self.build_system.specs       = self.fftw_binary.build_system.specs

    @sanity_function
    def assert_version(self):
        return sn.assert_found(r'FFTW version', self.stdout)
