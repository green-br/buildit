import os
import reframe as rfm
import reframe.utility.sanity as sn
from spack_base import SpackCompileOnlyBase

class OSUSpackBuild(SpackCompileOnlyBase):
    spackspec = 'osu-micro-benchmarks@7.5'

class OSUSpackCheckBase(rfm.RegressionTest):

    osu_binary = fixture(OSUSpackBuild, scope='environment')
    fullspackspec = variable(str)

    descr = 'OSU test using Spack'
    build_system = 'Spack'
    valid_systems = ['*']
    valid_prog_environs = ['*']

    benchmark = variable(str)

    exclusive_access = True
    extra_resources = {
        'memory': {'size': '4000'}
    }

    @run_after('setup')
    def set_environment(self):
        self.build_system.environment = os.path.join(self.osu_binary.stagedir, 'rfm_spack_env')
        self.build_system.specs       = self.osu_binary.build_system.specs
        self.fullspackspec            = ' '.join(self.osu_binary.build_system.specs)

    @run_before('run')
    def prepare_run(self):
        self.num_tasks = 2
        self.num_nodes = 2
        self.num_tasks_per_node = 1
        if self.metric == 'osu_allreduce':
            proc = self.current_partition.processor
            self.num_nodes = 2
            self.num_tasks = proc.num_cores

        self.executable = self.benchmark
        self.executable_opts = ['-x', '100', '-i', '1000']

    @sanity_function
    def validate_test(self):
        return sn.assert_found(r'^8', self.stdout)

    def _extract_metric(self, size):
        return sn.extractsingle(rf'^{size}\s+(\S+)', self.stdout, 1, float)

    @run_before('performance')
    def set_perf_vars(self):
        make_perf = sn.make_performance_function
        if self.metric == 'latency':
            self.perf_variables = {
                'latency': make_perf(self._extract_metric(8), 'us')
            }
        else:
            self.perf_variables = {
                'bandwidth': make_perf(self._extract_metric(1048576), 'MB/s')
            }

@rfm.simple_test
class OSUSpackCheckLatency(OSUSpackCheckBase):
    descr = 'OSU latency test'
    kind = 'pt2pt/standard'
    benchmark = 'osu_latency'
    metric = 'latency'
    executable_opts = ['-x', '3', '-i', '10']


@rfm.simple_test
class OSUSpackCheckBandwidth(OSUSpackCheckBase):
    descr = 'OSU bandwidth test'
    kind = 'pt2pt/standard'
    benchmark = 'osu_bw'
    metric = 'bandwidth'
    executable_opts = ['-x', '3', '-i', '10']


@rfm.simple_test
class OSUSpackCheckAllReduce(OSUSpackCheckBase):
    descr = 'OSU Allreduce test'
    kind = 'collective/blocking'
    benchmark = 'osu_allreduce'
    metric = 'bandwidth'
    executable_opts = ['-m', '8', '-x', '3', '-i', '10']
