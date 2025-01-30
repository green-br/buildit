import reframe as rfm
import os

class SpackCompileOnlyBase(rfm.CompileOnlyRegressionTest):
    descr = 'Base class to build from Spack'
    build_system = 'Spack'
    #valid_systems = ['*']
    #valid_prog_environs = ['gcc-12', 'gcc-13', 'cce-17']

    @run_before('compile')
    def setup_build_system(self):
        myrepos = self.current_environ.extras.get('myrepos')
        mycompile = self.current_environ.extras.get('mycompile')
        mypackage = self.current_environ.extras.get('mypackage')
        myspackcomp = self.current_environ.extras.get('myspackcomp')
        self.build_system.install_tree = os.getenv('HOME') + '/.reframe/opt/spack'
        self.build_system.config_opts = [f'repos:[{myrepos}]',
                                         f'view:true',
                                         f'concretizer:unify:true',
                                         f'concretizer:reuse:false']
        self.build_system.specs = [f'{self.spackspec} % {myspackcomp}']
        self.build_system.preinstall_cmds = ['export SPACK_DISABLE_LOCAL_CONFIG=true',
                                             f'spack -e rfm_spack_env config add -f "{mycompile}"',
                                             f'spack -e rfm_spack_env config add -f "{mypackage}"']

