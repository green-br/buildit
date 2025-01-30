site_configuration = {
    'storage' : [
        {
            'enabled': 'true'
        }
    ],
    'environments' : [
        {
            'name': 'gcc-12',
            'extras' : {
                'myrepos': '<location>/buildit/repo/v0.23/isamrepo',
                'mypackage': '<location>/buildit/config/3/v0.23/packages.yaml',
                'mycompile': '<location>/buildit/config/3/v0.23/linux/compilers.yaml',
                'myspackcomp': 'gcc@12.3'
            }
        },
        {
            'name': 'gcc-13',
            'extras' : {
                'myrepos': '<location>/buildit/repo/v0.23/isamrepo',
                'mypackage': '<location>/buildit/config/3/v0.23/packages.yaml',
                'mycompile': '<location>/buildit/config/3/v0.23/linux/compilers.yaml',
                'myspackcomp': 'gcc@13.2'
            }
        },
        {
            'name': 'cce-17',
            'extras' : {
                'myrepos': '<location>/buildit/repo/v0.23/isamrepo',
                'mypackage': '<location>/buildit/config/3/v0.23/packages.yaml',
                'mycompile': '<location>/buildit/config/3/v0.23/linux/compilers.yaml',
                'myspackcomp': 'cce@17.0.1'
            }
        }


    ],
    'systems': [
        {
            'name': 'i3',
            'descr': 'Isambard 3 Cluster',
            'hostnames': ['login02'],
            'partitions': [
                {
                    'name': 'login',
                    'descr': 'Login nodes',
                    'scheduler': 'local',
                    'launcher': 'local',
                    'environs': ['gcc-12','gcc-13','cce-17']
                },
                {
                    'name': 'grace',
                    'descr': 'Grace nodes',
                    'scheduler': 'squeue',
                    'launcher': 'srun',
                    'access': ['-p grace -t 01:00:00'],
                    'environs': ['gcc-12','gcc-13','cce-17'],
                    'resources': [
                        {
                            'name': 'memory',
                            'options': ['--mem={size}']
                        }
                    ]
                }
            ]
        }
    ]
}
