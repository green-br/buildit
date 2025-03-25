import reframe as rfm
import os

class SpackCompileOnlyBase(rfm.CompileOnlyRegressionTest):
    descr = 'Base class to build from Spack'
    build_system = 'Spack'
    sourcefile = None
    spackspec = variable(str)
    needsmpi  = variable(bool, value=True)
    env_spackspec = {}

    @run_before('compile')
    def setup_build_system(self):
        if self.sourcefile is not None:
            targetfile = os.path.join(self.stagedir, 
                                      os.path.basename(self.sourcefile))
            os.symlink(self.sourcefile,targetfile)

        myrepos = os.path.join(
            os.getenv('MYCONFDIR'),
            self.current_environ.extras.get('myrepos')
        )
        mycompile = os.path.join(
            os.getenv('MYCONFDIR'),
            self.current_environ.extras.get('mycompile')
        )
        mypackage = os.path.join(
            os.getenv('MYCONFDIR'),
            self.current_environ.extras.get('mypackage')
        )

        mympidep = ''
        myspackcomp = self.current_environ.extras.get('myspackcomp')
        if ( 'no-cray-mpich' in self.current_environ.features
            and self.needsmpi):
            mympidep = f'^mpich@4.3.0 % {myspackcomp}'
        if self.current_environ.name in self.env_spackspec:
            self.spackspec = f'{self.env_spackspec[self.current_environ.name]}'
        self.build_system.install_tree = os.getenv('HOME') + '/.reframe/opt/spack'
        self.build_system.config_opts = [f'repos:[{myrepos}]',
                                         f'view:true',
                                         f'concretizer:unify:true',
                                         f'concretizer:reuse:false']
        self.build_system.specs = [f'{self.spackspec} % {myspackcomp} {mympidep}']
        self.build_system.preinstall_cmds = ['export SPACK_DISABLE_LOCAL_CONFIG=true',
                                             f'spack -e rfm_spack_env config add -f "{mycompile}"',
                                             f'spack -e rfm_spack_env config add -f "{mypackage}"']

