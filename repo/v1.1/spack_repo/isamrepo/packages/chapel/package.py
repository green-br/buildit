# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_base import PackageBase # Or other base class

# Import the original Mpich class from the 'builtin' repository
from spack_repo.builtin.packages.chapel.package import Chapel as BuiltinChapel

from spack.package import *

class Chapel(BuiltinChapel):
    variant(
        "comm_ofi_oob",
        values=("sockets", "mpi", "pmi2"),
        default="sockets",
        description="Select out-of-band support",
        multi=False,
    )

    chpl_env_vars = [
        "CHPL_ATOMICS",
        "CHPL_AUX_FILESYS",
        "CHPL_COMM",
        "CHPL_COMM_OFI_OOB",
        "CHPL_COMM_SUBSTRATE",
        "CHPL_DEVELOPER",
        "CHPL_GASNET_SEGMENT",
        "CHPL_GMP",
        "CHPL_GPU",
        "CHPL_GPU_ARCH",
        "CHPL_GPU_MEM_STRATEGY",
        "CHPL_HOME",
        "CHPL_HOST_ARCH",
        # "CHPL_HOST_CC",
        "CHPL_HOST_COMPILER",
        # "CHPL_HOST_CXX",
        "CHPL_HOST_JEMALLOC",
        "CHPL_HOST_MEM",
        "CHPL_HOST_PLATFORM",
        "CHPL_HWLOC",
        "CHPL_LAUNCHER",
        "CHPL_LIB_PIC",
        "CHPL_LIBFABRIC",
        "CHPL_LLVM",
        "CHPL_LLVM_CONFIG",
        "CHPL_LLVM_SUPPORT",
        "CHPL_LLVM_VERSION",
        "CHPL_LOCALE_MODEL",
        "CHPL_MEM",
        "CHPL_RE2",
        "CHPL_SANITIZE",
        "CHPL_SANITIZE_EXE",
        "CHPL_TARGET_ARCH",
        # "CHPL_TARGET_CC",
        "CHPL_TARGET_COMPILER",
        "CHPL_TARGET_CPU",
        # "CHPL_TARGET_CXX",
        "CHPL_TARGET_PLATFORM",
        "CHPL_TASKS",
        "CHPL_TIMERS",
        "CHPL_UNWIND",
    ]


    def setup_run_environment(self, env: EnvironmentModifications) -> None:
        super().setup_run_environment(env) # Call parent method
        env.set("CHPL_RT_MAX_HEAP_SIZE", "10g")


