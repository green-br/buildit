import os
import reframe as rfm
import reframe.utility as util
import reframe.utility.sanity as sn
from spack_base import SpackCompileOnlyBase

class GromacsSpackBuild(SpackCompileOnlyBase):
    defspec = 'gromacs@2024.3'


# RegressionTest is used so Spack uses existing environment.
# This also uses same spec.
@rfm.simple_test
class GromacsSpackCheck(rfm.RegressionTest):

    gromacs_binary = fixture(GromacsSpackBuild, scope='environment')
    fullspackspec  = variable(str)
 
    descr = 'Gromacs test using Spack'
    build_system = 'Spack'
    valid_systems = ['*']

    valid_prog_environs = ['-no-gromacs']

    build_only = variable(int, value=0)
    num_nodes = parameter([1, 2, 4, 8, 16])
    num_threads = variable(int, value=1)
    exclusive_access = True
    extra_resources = {
        'memory': {'size': '0'}
    }

    #: The version of the benchmark suite to use.
    #:
    #: :type: :class:`str`
    #: :default: ``'1.0.0'``
    benchmark_version = variable(str, value='1.0.0', loggable=True)

    #: Parameter pack encoding the benchmark information.
    #:
    #: The first element of the tuple refers to the benchmark name,
    #: the second is the energy reference and the third is the
    #: tolerance threshold.
    #:
    #: :type: `Tuple[str, float, float]`
    #: :values:
    benchmark_info = parameter([
        #('HECBioSim/Crambin', -204107.0, 0.001)
        #('HECBioSim/Glutamine-Binding-Protein', -724598.0, 0.001),
        #('HECBioSim/hEGFRDimer', -3.32892e+06, 0.001),
        #('HECBioSim/hEGFRDimerSmallerPL', -3.27080e+06, 0.001),
        #('HECBioSim/hEGFRDimerPair', -1.20733e+07, 0.001),
        #('HECBioSim/hEGFRtetramerPair', -2.09831e+07, 0.001)
        ('GROMACS_TestCaseA', -1.50925e+06, 0.001),
        ('GROMACS_TestCaseB', -3.06407e+07, 0.001),
    ], fmt=lambda x: x[0], loggable=True)

    #: Parameter encoding the implementation of the non-bonded calculations
    #:
    #: :type: :class:`str`
    #: :values: ``['cpu', 'gpu']``
    #nb_impl = parameter(['cpu', 'gpu'], loggable=True)
    nb_impl = parameter(['cpu'], loggable=True)

    executable = 'gmx_mpi mdrun'
    keep_files = ['md.log']


    @run_after('init')
    def prepare_test(self):
        self.__bench, self.__nrg_ref, self.__nrg_tol = self.benchmark_info
        self.descr = f'GROMACS {self.__bench} benchmark (NB: {self.nb_impl})'
        if self.__bench.startswith("HEC"):
            self.prerun_cmds.extend([
                f'curl -LJO https://github.com/victorusu/GROMACS_Benchmark_Suite/raw/{self.benchmark_version}/{self.__bench}/benchmark.tpr'  # noqa: E501
            ])
        else:
            self.prerun_cmds.append([
                f'curl -LJO https://repository.prace-ri.eu/ueabs/GROMACS/2.2/{self.__bench}.tar.xz',
                f'tar xvf {self.__bench}.tar.xz --strip-components 1',
            ])
            self.executable_opts += ['-cpt', '1000', '-maxh', '1.0', '-nsteps', '50000' ] 

         

        self.executable_opts += ['-nb', self.nb_impl, '-s *.tpr']

    @run_after('setup')
    def set_environment(self):
        self.skip_if(
            self.num_nodes > self.current_partition.extras.get('max_nodes',128),
            'exceeded node limit'
        )
        self.build_system.environment = os.path.join(self.gromacs_binary.stagedir, 'rfm_spack_env')
        self.build_system.specs       = self.gromacs_binary.build_system.specs
        self.fullspackspec            = ' '.join(self.gromacs_binary.build_system.specs)

    @run_before('run')
    def set_job_size(self):
        self.skip_if( self.build_only == 1, 'build only')
        proc = self.current_partition.processor
        self.num_tasks_per_node = proc.num_cores
        if self.num_threads:
            self.num_tasks_per_node = (proc.num_cores) // self.num_threads
            self.env_vars['OMP_NUM_THREADS'] = self.num_threads
        self.num_tasks = self.num_tasks_per_node * self.num_nodes


    @loggable
    @property
    def bench_name(self):
        '''The benchmark name.

        :type: :class:`str`
        '''

        return self.__bench

    @property
    def energy_ref(self):
        '''The energy reference value for this benchmark.

        :type: :class:`str`
        '''
        return self.__nrg_ref

    @property
    def energy_tol(self):
        '''The energy tolerance value for this benchmark.

        :type: :class:`str`
        '''
        return self.__nrg_tol

    @performance_function('ns/day')
    def perf(self):
        return sn.extractsingle(r'Performance:\s+(?P<perf>\S+)',
                                'md.log', 'perf', float)

    @deferrable
    def energy_hecbiosim_crambin(self):
        return sn.extractsingle(r'\s+Potential\s+Kinetic En\.\s+Total Energy'
                                r'\s+Conserved En\.\s+Temperature\n'
                                r'(\s+\S+){2}\s+(?P<energy>\S+)(\s+\S+){2}\n'
                                r'\s+Pressure \(bar\)\s+Constr\. rmsd',
                                'md.log', 'energy', float, item=-1)

    @deferrable
    def energy_hecbiosim_glutamine_binding_protein(self):
        return sn.extractsingle(r'\s+Potential\s+Kinetic En\.\s+Total Energy'
                                r'\s+Conserved En\.\s+Temperature\n'
                                r'(\s+\S+){2}\s+(?P<energy>\S+)(\s+\S+){2}\n'
                                r'\s+Pressure \(bar\)\s+Constr\. rmsd',
                                'md.log', 'energy', float, item=-1)

    @deferrable
    def energy_hecbiosim_hegfrdimer(self):
        return sn.extractsingle(r'\s+Potential\s+Kinetic En\.\s+Total Energy'
                                r'\s+Conserved En\.\s+Temperature\n'
                                r'(\s+\S+){2}\s+(?P<energy>\S+)(\s+\S+){2}\n'
                                r'\s+Pressure \(bar\)\s+Constr\. rmsd',
                                'md.log', 'energy', float, item=-1)

    @deferrable
    def energy_hecbiosim_hegfrdimersmallerpl(self):
        return sn.extractsingle(r'\s+Potential\s+Kinetic En\.\s+Total Energy'
                                r'\s+Conserved En\.\s+Temperature\n'
                                r'(\s+\S+){2}\s+(?P<energy>\S+)(\s+\S+){2}\n'
                                r'\s+Pressure \(bar\)\s+Constr\. rmsd',
                                'md.log', 'energy', float, item=-1)

    @deferrable
    def energy_hecbiosim_hegfrdimerpair(self):
        return sn.extractsingle(r'\s+Potential\s+Kinetic En\.\s+Total Energy'
                                r'\s+Conserved En\.\s+Temperature\n'
                                r'(\s+\S+){2}\s+(?P<energy>\S+)(\s+\S+){2}\n'
                                r'\s+Pressure \(bar\)\s+Constr\. rmsd',
                                'md.log', 'energy', float, item=-1)

    @deferrable
    def energy_hecbiosim_hegfrtetramerpair(self):
        return sn.extractsingle(r'\s+Potential\s+Kinetic En\.\s+Total Energy'
                                r'\s+Conserved En\.\s+Temperature\n'
                                r'(\s+\S+){2}\s+(?P<energy>\S+)(\s+\S+){2}\n'
                                r'\s+Pressure \(bar\)\s+Constr\. rmsd',
                                'md.log', 'energy', float, item=-1)
    
    @deferrable
    def energy_gromacs_testcasea(self):
        return sn.extractsingle(r'\s+Coul\. recip\.\s+Potential\s+Kinetic En\.\s+Total Energy'
                                r'\s+Conserved En\.\n'
                                r'(\s+\S+){3}\s+(?P<energy>\S+)(\s+\S+){1}\n'
                                r'\s+Temperature\s+Pres\. DC \(bar\)\s+Pressure \(bar\)\s+Constr\. rmsd',
                                'md.log', 'energy', float, item=-1)

    
    @deferrable
    def energy_gromacs_testcaseb(self):
        return sn.extractsingle(r'\s+LJ \(SR\)\s+Coulomb \(SR\)\s+Potential'
                                r'\s+Kinetic En\.\s+Total Energy\n'
                                r'(\s+\S+){4}\s+(?P<energy>\S+)\n'
                                r'\s+Conserved En\.\s+Temperature'
                                r'\s+Pressure \(bar\)\s+Constr\. rmsd',
                                'md.log', 'energy', float, item=-1)

    @sanity_function
    def assert_energy_readout(self):
        '''Assert that the obtained energy meets the benchmark tolerances.'''

        energy_fn_name = f'energy_{util.toalphanum(self.__bench).lower()}'
        energy_fn = getattr(self, energy_fn_name, None)
        sn.assert_true(
            energy_fn is not None,
            msg=(f"cannot extract energy for benchmark {self.__bench!r}: "
                 f"please define a member function '{energy_fn_name}()'")
        ).evaluate()
        energy = energy_fn()
        energy_diff = sn.abs(energy - self.energy_ref)
        return sn.all([
            sn.assert_found('Finished mdrun', 'md.log'),
            sn.assert_reference(energy, self.energy_ref,
                                -self.energy_tol, self.energy_tol)
        ])
