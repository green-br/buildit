import os
import reframe as rfm
import reframe.utility.sanity as sn
from spack_base import SpackCompileOnlyBase

class StreamSpackBuild(SpackCompileOnlyBase):
    executable = 'stream_c.exe'
    spackspec = 'stream@5.10 +openmp stream_array_size=120000000 ntimes=200'
    env_spackspec = { 'cce-17-macs':'stream@5.10 +openmp stream_array_size=120000000 ntimes=200 cflags=-mcmodel=medium' }

@rfm.simple_test
class StreamSpackCheck(rfm.RegressionTest):

    stream_binary = fixture(StreamSpackBuild, scope='environment')

    descr = 'Stream test using Spack'
    build_system = 'Spack'
    valid_systems = ['*']
    valid_prog_environs = ['*']

    num_percent = parameter([25, 50, 75, 100])
    thread_placement = parameter(['close', 'cores', 'spread'])

    exclusive_access = True
    extra_resources = {
        'memory': {'size': '4000'}
    }

    @run_after('setup')
    def set_environment(self):
        self.executable = self.stream_binary.executable
        self.build_system.environment = os.path.join(self.stream_binary.stagedir, 'rfm_spack_env')
        self.build_system.specs       = self.stream_binary.build_system.specs

    @run_before('run')
    def setup_threading(self):
        proc = self.current_partition.processor
        self.num_threads = int(proc.num_cores * self.num_percent ) // 100
        self.num_cpus_per_task = proc.num_cores

        self.env_vars['OMP_NUM_THREADS'] = self.num_threads
        self.env_vars['OMP_PROC_BIND'] = self.thread_placement

    @sanity_function
    def validate(self):
        return sn.assert_found(r'Solution Validates', self.stdout)

    @performance_function('MB/s')
    def copy_bw(self):
        return sn.extractsingle(r'Copy:\s+(\S+)', self.stdout, 1, float)

    @performance_function('MB/s')
    def triad_bw(self):
        return sn.extractsingle(r'Triad:\s+(\S+)', self.stdout, 1, float)
  
