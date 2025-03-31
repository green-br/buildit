import os
import statistics
import reframe as rfm
import reframe.utility.sanity as sn
from spack_base import SpackCompileOnlyBase

class ArmKernelsSpackBuild(SpackCompileOnlyBase):
    defspec = 'arm-kernels@main'
    needsmpi = False

class ArmKernelsSpackCheckBase(rfm.RegressionTest):

    armkernel_binary = fixture(ArmKernelsSpackBuild, scope='environment')
    fullspackspec = variable(str)

    descr = 'Arm-kernels test using Spack'
    build_system = 'Spack'
    valid_systems = ['*']
    valid_prog_environs = ['gcc-12']

    benchmark = variable(str)

    exclusive_access = True
    extra_resources = {
        'memory': {'size': '0'}
    }

    @run_after('setup')
    def set_environment(self):
        self.build_system.environment = os.path.join(self.armkernel_binary.stagedir, 'rfm_spack_env')
        self.build_system.specs       = self.armkernel_binary.build_system.specs
        self.fullspackspec            = ' '.join(self.armkernel_binary.build_system.specs)

    @run_before('run')
    def prepare_run(self):
        self.job.launcher.options = ['--cpu-bind=map_cpu:$CPUID']
        
        proc = self.current_partition.processor
        self.num_tasks = 1
        max_cpuid=proc.num_cores-1
        self.prerun_cmds = [f'for CPUID in `seq 0 {max_cpuid}`; do']
        self.postrun_cmds = ['done']
        self.executable = f'{self.benchmark}.x'

    @sanity_function
    def validate_test(self):
        return sn.assert_found(r'^GOps/sec', self.stdout)
    
    @sn.deferrable
    def _operation_per_second_avg(self):
        ops = sn.extractall(r'GOps/sec;(\S+)', self.stdout, 1, float)
        return statistics.mean(ops.evaluate())

    @sn.deferrable
    def _operation_per_second_dev(self):
        ops = sn.extractall(r'GOps/sec;(\S+)', self.stdout, 1, float)
        return statistics.stdev(ops.evaluate())

        #avg = sn.avg(ops)
        #stdev = 0
        #for x in ops:
        #    stdev += (x-avg)**2
        #stdev = stdev / sn.len(ops)
        #return stdev

   
    @run_before('performance')
    def set_perf_vars(self):
        make_perf = sn.make_performance_function
        self.perf_variables = {
            'mean': make_perf(self._operation_per_second_avg(), 'GOps/s'),
            'stdev': make_perf(self._operation_per_second_dev(), 'GOps/s'),
        }
       
@rfm.simple_test
class ArmKernelsSpackCheckFp64SveFmul(ArmKernelsSpackCheckBase):
    descr = 'fp64_sve_fmul'
    benchmark = 'fp64_sve_fmul'


@rfm.simple_test
class ArmKernelsSpackCheckFp64NeonFmul(ArmKernelsSpackCheckBase):
    descr = 'fp64_neon_fmul'
    benchmark = 'fp64_neon_fmul'

@rfm.simple_test
class ArmKernelsSpackCheckFp64ScalarFmul(ArmKernelsSpackCheckBase):
    descr = 'fp64_scalar_fmul'
    benchmark = 'fp64_scalar_fmul'

@rfm.simple_test
class ArmKernelsSpackCheckFp64SvePredFmla(ArmKernelsSpackCheckBase):
    descr = 'fp64_sve_pred_fmla'
    benchmark = 'fp64_sve_pred_fmla'
