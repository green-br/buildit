# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *

class ArmKernels(MakefilePackage):
    """Optimized primitives for collective multi-GPU communication."""

    homepage = "https://github.com/NVIDIA/arm-kernels"
    git = "https://github.com/NVIDIA/arm-kernels.git"
    maintainers("green-br")

    version("main", branch="main")
    depends_on("cxx", type="build")

    def patch(self):
        filter_file(
            r"CXX = .*",
            "", 
            "config.mk",
        )
        filter_file(
            r"CXXFLAGS = .*",
            "",
            "config.mk",
        )
        target = self.spec.target
        if "sve" not in target.features:
            filter_file(
                r"^.*_sve_.*\.x.*",
                "	\\",
                "arithmetic/Makefile",
            )
        if "fphp" not in target.features:
            filter_file(
                r"^.*fp16_.*\.x.*",
                "	\\",
                "arithmetic/Makefile",
            )



    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install_tree("arithmetic", prefix.bin)

