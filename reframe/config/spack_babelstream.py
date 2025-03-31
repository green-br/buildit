import os
import reframe as rfm
import reframe.utility.sanity as sn
from spack_base import SpackCompileOnlyBase

class BabelStreamSpackBuild(SpackCompileOnlyBase):
    executable = 'omp-stream'
    # stream_array_size is calculated as 2.7GB per Grace CPU
    defspec = 'babelstream@5.0 +omp'
    needsmpi = False

@rfm.simple_test
class BabelStreamSpackCheck(rfm.RegressionTest):

    binary = fixture(BabelStreamSpackBuild, scope='environment')
    fullspackspec = variable(str)

    descr = 'Stream test using Spack'
    build_system = 'Spack'
    valid_systems = ['*']
    valid_prog_environs = ['*']

    num_percent = parameter([25, 50, 75, 100])
    thread_placement = parameter(['true', 'close', 'spread'])

    exclusive_access = True
    extra_resources = {
        'memory': {'size': '0'}
    }

    @run_after('setup')
    def set_environment(self):
        self.executable = self.binary.executable
        self.build_system.environment = os.path.join(self.binary.stagedir, 'rfm_spack_env')
        self.build_system.specs       = self.binary.build_system.specs
        self.fullspackspec            = ' '.join(self.binary.build_system.specs)
        self.executable_opts = ['--arraysize', '240000000', '--numtimes', '200']

    @run_before('run')
    def setup_threading(self):
        proc = self.current_partition.processor
        self.num_threads = int(proc.num_cores * self.num_percent ) // 100
        self.num_cpus_per_task = proc.num_cores

        self.env_vars['OMP_NUM_THREADS'] = self.num_threads
        self.env_vars['OMP_PLACES'] = 'cores'
        self.env_vars['OMP_PROC_BIND'] = self.thread_placement

    @sanity_function
    def validate(self):
        return sn.assert_not_found(r'Validation failed', self.stdout)

    @performance_function('MB/s')
    def copy_bw(self):
        return sn.extractsingle(r'Copy\s+(\S+)', self.stdout, 1, float)

    @performance_function('MB/s')
    def triad_bw(self):
        return sn.extractsingle(r'Triad\s+(\S+)', self.stdout, 1, float)
  
