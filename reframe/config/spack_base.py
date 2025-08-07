import reframe as rfm
import os

class SpackCompileOnlyBase(rfm.CompileOnlyRegressionTest):
    descr = 'Base class to build from Spack'
    build_system = 'Spack'
    sourcefile = None
    defspec = variable(str)
    defdeps = variable(str, value="")
    mpidep  = variable(str, value="")
    needsmpi  = variable(bool, value=True)
    env_spackspec = {}
    extra_resources = {
        'memory': {'size': '0'}
    }

    @run_before('compile')
    def setup_build_system(self):
        if self.build_locally == 0:
            self.skip_if( self.current_partition.scheduler.is_local,
                'ingore local if building locally on scheduler'
            )
        # Quick fix to build more on MACS

        self.build_job.options = ['-c 16']

        if self.sourcefile is not None:
            targetfile = os.path.join(self.stagedir, 
                                      os.path.basename(self.sourcefile))
            os.symlink(self.sourcefile,targetfile)

        myrepos = os.path.join(
            os.getenv('MYCONFDIR'),
            self.current_environ.extras.get('myrepos')
        )
        mypackage = os.path.join(
            os.getenv('MYCONFDIR'),
            self.current_environ.extras.get('mypackage')
        )

        mynvlocalrc = None
        if self.current_environ.extras.get('mynvlocalrc', None):
            mynvlocalrc = os.path.join(
                os.getenv('MYCONFDIR'),
                self.current_environ.extras.get('mynvlocalrc')
            )

        myspackcomp = self.current_environ.extras.get('myspackcomp')
        
        if self.mpidep:
            self.mpidep = f'{self.mpidep} % {myspackcomp}'
        if ( 'no-cray-mpich' in self.current_environ.features
            and self.needsmpi and not self.mpidep):
            self.mpidep = f'^mpich@4.3.0 % {myspackcomp}'

        spec   = self.defspec
        deps   = f'{self.mpidep} {self.defdeps}'

        if self.current_environ.name in self.env_spackspec:
            spec = f"{self.env_spackspec[self.current_environ.name]['spec']}"
            deps = f"{self.env_spackspec[self.current_environ.name].get('deps','')}"
        self.build_system.install_tree = os.getenv('HOME') + f'/.reframe/opt/spack-1.0/'

        self.build_system.config_opts = [f'repos:[{myrepos}]',
                                         f'config:build_jobs:8',
                                         f'view:true',
                                         f'concretizer:unify:true',
                                         f'concretizer:reuse:false']

        self.build_system.specs = [f'{spec} % {myspackcomp} {deps}']

        self.build_system.preinstall_cmds = ['export SPACK_DISABLE_LOCAL_CONFIG=true',
                                             f'spack -e rfm_spack_env config add -f "{mypackage}"',
                                             f'spack -e rfm_spack_env concretize -f']
        if mynvlocalrc:
            self.build_system.preinstall_cmds.append(f'export NVLOCALRC={mynvlocalrc}')

