import os
import reframe as rfm
import reframe.utility.sanity as sn
from spack_base import SpackCompileOnlyBase

class BZip2SpackBuild(SpackCompileOnlyBase):
    executable = 'bzip2'
    spackspec = 'bzip2@1.0.6'

@rfm.simple_test
class BZip2SpackCheck(rfm.RegressionTest):
    descr = 'Demo test using Spack to run the test code'
    build_system = 'Spack'
    valid_systems = ['*']
    valid_prog_environs = ['*']
    executable = 'bzip2'
    executable_opts = ['--help']
    bzip2_binary = fixture(BZip2SpackBuild, scope='environment')

    @run_after('setup')
    def set_environment(self):
        self.build_system.environment = os.path.join(self.bzip2_binary.stagedir, 'rfm_spack_env')
        self.build_system.specs       = self.bzip2_binary.build_system.specs

    @sanity_function
    def assert_version(self):
        return sn.assert_found(r'Version 1.0.6', self.stderr)
