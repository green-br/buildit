# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *

class HwSmi(MakefilePackage):
    """A minimal, cross-compatible CPU/GPU telemetry monitor with accurate 
       data directly from vendor APIs and beautiful ASCII visualization."""

    homepage = "https://github.com/ProjectPhysX/hw-smi"
    git = "https://github.com/ProjectPhysX/hw-smi.git"
    url = "https://github.com/ProjectPhysX/hw-smi/archive/v1.0.tar.gz"
    maintainers("green-br")

    version("master", branch="master")
    version("1.2", sha256="79fc6665e10c77a05807146ed74260948488adf6199a38e55ba6b403db90e3b8")
    version("1.1", sha256="9d7a6362eafe983432c289c2aa47658dd36d1a7a731379883ad116284cc90da3")
    version("1.0", sha256="83da552d242af9898e7d1b5b448a2b0bce391eefcd6af0fc5ef0cd481f68744e")

    variant("gpu", default="none",
            values=("none", "nvidia", "amd", "intel"),
            multi=True)

    depends_on("cxx", type="build")
    
    def edit(self, spec, prefix):
        flags = []
        flags.append(self.compiler.cxx17_flag)

        if self.spec.satisfies("gpu=nvidia"):
            flags.append("-DNVIDIA_GPU -lnvidia-ml")
        if self.spec.satisfies("gpu=amd"):
            flags.append("-DAMD_GPU -lamd_smi")
        if self.spec.satisfies("gpu=intel"):
            flags.append("-DINTEL_GPU -lze_intel_gpu")

        config = [
            f"CXX = {spack_cxx}",
            f"CXXFLAGS = {' '.join(flags)}",
            "hw-smi: src/main.cpp",
            "\t$(CXX) $< -o $@ $(CXXFLAGS)",
        ]

        with open("Makefile", "w") as mf:
            for var in config:
                mf.write(f"{var}\n")

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install("hw-smi", prefix.bin)

