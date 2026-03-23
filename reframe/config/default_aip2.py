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
                'myrepos': 'buildit/repo/v1.1/spack_repo/isamrepo',
                'mypackage': 'buildit/config/aip2/v1.1/packages.yaml',
                'myspackcomp': 'gcc@12.3.0'
            }
        },
        {
            'name': 'gcc-13',
            'extras' : {
                'myrepos': 'buildit/repo/v1.1/spack_repo/isamrepo',
                'mypackage': 'buildit/config/aip2/v1.1/packages.yaml',
                'myspackcomp': 'gcc@13.3.1'
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
                'myrepos': 'buildit/repo/v1.1/spack_repo/isamrepo',
                'mypackage': 'buildit/config/aip2/v1.1/packages.yaml',
                'myspackcomp': 'cce@18.0.0'
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
                'myrepos': 'buildit/repo/v1.1/spack_repo/isamrepo',
                'mypackage': 'buildit/config/aip2/v1.1/packages.yaml',
                'myspackcomp': 'nvhpc@24.11'
            }
        },
    ],
    'systems': [
        {
            'name': 'aip2',
            'descr': 'Isambard-AI Phase 2 Cluster',
            'hostnames': ['login4[0-9]'],
            'env_vars': [ 
                ['MYCONFDIR','$HOME/git']
            ],
            'partitions': [
                {
                    'name': 'login',
                    'descr': 'Login nodes',
                    'scheduler': 'local',
                    'launcher': 'local',
                    'environs': ['gcc-12','gcc-13','cce-18','nvhpc-24']
                },
                {
                    'name': 'workq',
                    'descr': 'Workq nodes',
                    'scheduler': 'slurm',
                    'launcher': 'srun',
                    'access': [
                        '-p workq',
                        '-t 02:00:00',
                    ],
                    'environs': ['gcc-12','gcc-13','cce-18','nvhpc-24'],
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
                        'max_nodes': 128,
                    },
                },
            ]
        },
    ]
}
