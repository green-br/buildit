# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

class Minibude(CMakePackage):
    """implementation of the core computation of the Bristol University 
    Docking Engine (BUDE) in different HPC programming models"""

    homepage = "https://github.com/UoB-HPC/miniBUDE"
    git = "https://github.com/UoB-HPC/miniBUDE.git"
    #git = "https://github.com/green-br/miniBUDE.git"

    maintainers("green-br")

    license("Apache-2.0", checked_by="green-br")

    version("main",  branch="test-compiler-options")

    variant(
        "model", default="serial", description="Implementation to build",
        values=("omp", "serial"), multi=False
    )

    def cmake_args(self):
        args = ["--trace","-DRELEASE_FLAGS=-O3;-ffast-math"]
        #args = []
        if self.spec.variants["model"].value == "serial":
            args.append("-DMODEL=serial")
        elif self.spec.variants["model"].value == "omp":
            args.append("-DMODEL=omp")

        return args
