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
    'logging' : [
        {
            'handlers_perflog' : [
				{
                    'type': 'filelog',
                    'prefix': '%(check_system)s/%(check_partition)s',
                    'level': 'info',
                    'format': ('%(check_result)s|'
                               '%(check_job_completion_time)s|%(check_#ALL)s'),
                    'ignore_keys': [
                        'check_build_locally',
                        'check_build_time_limit',
                        'check_display_name',
                        'check_executable',
                        'check_executable_opts',
                        'check_hashcode',
                        'check_keep_files',
                        'check_local',
                        'check_maintainers',
                        'check_max_pending_time',
                        'check_outputdir',
                        'check_prebuild_cmds',
                        'check_prefix',
                        'check_prerun_cmds',
                        'check_postbuild_cmds',
                        'check_postrun_cmds',
                        'check_readonly_files',
                        'check_sourcepath',
                        'check_sourcesdir',
                        'check_stagedir',
                        'check_strict_check',
                        'check_tags',
                        'check_time_limit',
                        'check_valid_prog_environs',
                        'check_valid_systems',
                        'check_variables'
                    ],
                    'format_perfvars': (
                        '%(check_perf_value)s|%(check_perf_unit)s|'
                        '%(check_perf_ref)s|%(check_perf_lower_thres)s|'
                        '%(check_perf_upper_thres)s|'
                    ),
                    'append': False
                }
            ]
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
            'features': [
                'no-castep',
                'no-cp2k',
                'no-gromacs',
                'no-openfoam',
                'no-namd',
            ],
            'extras' : {
                'myrepos': 'buildit/repo/v0.23/isamrepo',
                'mypackage': 'buildit/config/3/v0.23/packages.yaml',
                'mycompile': 'buildit/config/3/v0.23/linux/compilers.yaml',
                'myspackcomp': 'cce@18.0.0'
            }
        },
        {
            'name': 'arm-24',
            'features': [
                'no-cray-mpich',
                'no-castep',
                'no-cp2k',
                'no-openfoam',
                'no-namd',
            ],
            'extras' : {
                'myrepos': 'buildit/repo/v0.23/isamrepo',
                'mypackage': 'buildit/config/3/v0.23/packages.yaml',
                'mycompile': 'buildit/config/3/v0.23/linux/compilers.yaml',
                'myspackcomp': 'arm@24.10.1'
            }
        },
        {
            'name': 'nvhpc-24',
            'features': [
                'no-castep',
                'no-cp2k',
                'no-openfoam',
                'no-namd',
            ],
            'extras' : {
                'myrepos': 'buildit/repo/v0.23/isamrepo',
                'mypackage': 'buildit/config/3/v0.23/packages.yaml',
                'mycompile': 'buildit/config/3/v0.23/linux/compilers.yaml',
                'mynvlocalrc': 'buildit/config/3/nvlocalrc/localrc',
                'myspackcomp': 'nvhpc@24.3'
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
            'features': [
                'no-castep',
                'no-cp2k',
                'no-gromacs',
                'no-openfoam',
                'no-namd',
            ],
            'extras' : {
                'myrepos': 'buildit/repo/v0.23/isamrepo',
                'mypackage': 'buildit/config/macs3/v0.23/packages.yaml',
                'mycompile': 'buildit/config/macs3/v0.23/linux/compilers.yaml',
                'myspackcomp': 'cce@17.0.1'
            }
        },
        {
            'name': 'rocm-5-macs',
            'features': [
                'no-cray-mpich',
                'no-castep',
                'no-cp2k',
                'no-gromacs',
                'no-namd',
                'no-openfoam',
            ],            
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
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': [
                        '-p milan',
                        '-t 02:00:00',
                    ],
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
                    ],
                    'extras': {
                        'max_nodes': 4,
                    },
                },
                {
                    'name': 'genoa',
                    'descr': 'Genoa nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': [
                        '-p genoa',
                        '-t 02:00:00',
                    ],
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

                    ],
                    'extras': {
                        'max_nodes': 2,
                    },
                },
                {
                    'name': 'berg',
                    'descr': 'Bergamo nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': [
                        '-p berg',
                        '-t 02:00:00',
                    ],
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
                    ],
                    'extras': {
                        'max_nodes': 2,
                    },
                },
                {
                    'name': 'spr',
                    'descr': 'Sapphire Rapids nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': [
                        '-p spr',
                        '-t 02:00:00',
                    ],
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

                    ],
                    'extras': {
                        'max_nodes': 2,
                    },
                },
                {
                    'name': 'sprhbm',
                    'descr': 'Sapphire Rapids HBM nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': [
                        '-p sprhbm',
                        '-t 02:00:00',
                    ],
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

                    ],
                    'extras': {
                        'max_nodes': 2,
                    },
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
                    'environs': ['gcc-12','gcc-13','cce-18','arm-24','nvhpc-24']
                },
                {
                    'name': 'grace',
                    'descr': 'Grace nodes',
                    'scheduler': 'slurm',
                    'sched_options': {
                        'use_nodes_option': True,
                    },
                    'launcher': 'srun',
                    'access': [
                        '-p grace',
                        '-t 02:00:00',
                    ],
                    'environs': ['gcc-12','gcc-13','cce-18','arm-24','nvhpc-24'],
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
