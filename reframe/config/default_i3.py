site_configuration = {

    'general' : [
        {
            'remote_detect': True
        }
    ],
    'storage' : [
        {
            'enable': True
        }
    ],
    'environments' : [
        {
            'name': 'gcc-12',
            'extras' : {
                'myrepos': 'buildit/repo/v0.23/isamrepo',
                'mypackage': 'buildit/config/3/v0.23/packages.yaml',
                'mycompile': 'buildit/config/3/v0.23/linux/compilers.yaml',
                'myspackcomp': 'gcc@12.3'
            }
        },
        {
            'name': 'gcc-13',
            'extras' : {

                'myrepos': 'buildit/repo/v0.23/isamrepo',
                'mypackage': 'buildit/config/3/v0.23/packages.yaml',
                'mycompile': 'buildit/config/3/v0.23/linux/compilers.yaml',
                'myspackcomp': 'gcc@13.2'
            }
        },
        {
            'name': 'cce-18',
            'extras' : {
                'myrepos': 'buildit/repo/v0.23/isamrepo',
                'mypackage': 'buildit/config/3/v0.23/packages.yaml',
                'mycompile': 'buildit/config/3/v0.23/linux/compilers.yaml',
                'myspackcomp': 'cce@18.0.0'
            }
        },
        {
            'name': 'arm-24',
            'extras' : {
                'myrepos': 'buildit/repo/v0.23/isamrepo',
                'mypackage': 'buildit/config/3/v0.23/packages.yaml',
                'mycompile': 'buildit/config/3/v0.23/linux/compilers.yaml',
                'myspackcomp': 'arm@24.10.1'
            }
        },
        {
            'name': 'gcc-12-macs',
            'extras' : {
                'myrepos': 'buildit/repo/v0.23/isamrepo',
                'mypackage': 'buildit/config/macs3/v0.23/packages.yaml',
                'mycompile': 'buildit/config/macs3/v0.23/linux/compilers.yaml',
                'myspackcomp': 'gcc@12.3'
            }
        },
        {
            'name': 'gcc-13-macs',
            'extras' : {
                'myrepos': 'buildit/repo/v0.23/isamrepo',
                'mypackage': 'buildit/config/macs3/v0.23/packages.yaml',
                'mycompile': 'buildit/config/macs3/v0.23/linux/compilers.yaml',
                'myspackcomp': 'gcc@13.2'
            }
        },
        {
            'name': 'cce-17-macs',
            'extras' : {
                'myrepos': 'buildit/repo/v0.23/isamrepo',
                'mypackage': 'buildit/config/macs3/v0.23/packages.yaml',
                'mycompile': 'buildit/config/macs3/v0.23/linux/compilers.yaml',
                'myspackcomp': 'cce@17.0.1'
            }
        },
        {
            'name': 'rocm-5-macs',
            'extras' : {
                'myrepos': 'buildit/repo/v0.23/isamrepo',
                'mypackage': 'buildit/config/macs3/v0.23/packages.yaml',
                'mycompile': 'buildit/config/macs3/v0.23/linux/compilers.yaml',
                'myspackcomp': 'rocmcc@5.7.0'
            }
        }
    ],
    'systems': [
        {
            'name': 'i3macs',
            'descr': 'Isambard 3 MACS Cluster',
            'hostnames': ['login05', 'login06'],
            'env_vars': [ 
                ['MYCONFDIR','$HOME/git']
            ],
            'partitions': [
                {
                    'name': 'login_macs',
                    'descr': 'MACS Login nodes',
                    'scheduler': 'local',
                    'launcher': 'local',
                    'environs': ['gcc-12-macs','gcc-13-macs','cce-17-macs']
                },
                {
                    'name': 'milan',
                    'descr': 'Milan nodes',
                    'scheduler': 'squeue',
                    'launcher': 'srun',
                    'access': ['-p milan -t 01:00:00'],
                    'environs': ['gcc-12-macs','gcc-13-macs','cce-17-macs'],
                    'resources': [
                        {
                            'name': 'memory',
                            'options': ['--mem={size}']
                        },
                        {
                            'name': 'network',
                            'options': ['--network={type}']
                        }

                    ]
                },
                {
                    'name': 'berg',
                    'descr': 'Bergamo nodes',
                    'scheduler': 'squeue',
                    'launcher': 'srun',
                    'access': ['-p berg -t 01:00:00'],
                    'environs': ['gcc-12-macs','gcc-13-macs','cce-17-macs'],
                    'resources': [
                        {
                            'name': 'memory',
                            'options': ['--mem={size}']
                        },
                        {
                            'name': 'network',
                            'options': ['--network={type}']
                        }

                    ]
                }

            ]
        },
        {
            'name': 'i3',
            'descr': 'Isambard 3 Cluster',
            'hostnames': ['login01','login02'],
            'env_vars': [ 
                ['MYCONFDIR','$HOME/git']
            ],
            'partitions': [
                {
                    'name': 'login',
                    'descr': 'Login nodes',
                    'scheduler': 'local',
                    'launcher': 'local',
                    'environs': ['gcc-12','gcc-13','cce-18','arm-24']
                },
                {
                    'name': 'grace',
                    'descr': 'Grace nodes',
                    'scheduler': 'squeue',
                    'launcher': 'srun',
                    'access': ['-p grace -t 01:00:00'],
                    'environs': ['gcc-12','gcc-13','cce-18','arm-24'],
                    'resources': [
                        {
                            'name': 'memory',
                            'options': ['--mem={size}']
                        },
                        {
                            'name': 'network',
                            'options': ['--network={type}']
                        }
                    ]
                }
            ]
        }
    ]
}
