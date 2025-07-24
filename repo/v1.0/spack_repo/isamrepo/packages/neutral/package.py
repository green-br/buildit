# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *


class Neutral(MakefilePackage):
    """
    A Monte Carlo Neutron Transport Mini-App
    """

    homepage = "https://github.com/UoB-HPC/neutral"
    git = "https://github.com/green-br/neutral.git"

    maintainers("green-br")

    version("master", commit="c50e50fcd903104bf9ad3ac7b84a27ba4428bef1", submodules=True)

    depends_on("c", type="build")  # generated

    depends_on("mpi", when="+mpi")

    variant("openmp", default=True, description="Build with OpenMP support")
    variant("mpi", default=True, description="Build with MPI support.")
    
    # Cloverleaf_ref Makefile contains some but not all required options for each compiler.
    # This package.py inserts what is needed for Intel, AOCC, and LLVM compilers.
    @property
    def build_targets(self):

        targets = []

        targets.append("KERNELS=omp3")
        targets.append("MPI=yes")
        targets.append("ARCH_COMPILER_CC={0}".format(self.spec["mpi"].mpicc))

        # Work around for bug in Makefiles for versions 1.3 and 1.1 (mis-defined as -openmp)
        if self.spec.satisfies("%intel"):
            targets.append("COMPILER=INTEL")

        # Work around for missing AOCC compilers option in Makefiles for versions 1.3 and 1.1
        elif self.spec.satisfies("%aocc"):
            targets.append("COMPILER=AOCC")
            targets.append("CFLAGS_AOCC=-fopenmp")

        # Work around for missing CLANG entries in Makefiles for master branch (commit:0fdb917),
        # and for versions 1.3 and 1.1
        elif self.spec.satisfies("%clang"):
            targets.append("COMPILER=CLANG")
            targets.append("CFLAGS_CLANG=-fopenmp")

        elif self.spec.satisfies("%gcc"):
            targets.append("COMPILER=GNU")
            targets.append("CFLAGS_GNU=-fopenmp")

        elif self.spec.satisfies("%cce"):
            targets.append("COMPILER=CRAY")
            targets.append("CFLAGS_CRAY=-fopenmp")
       
        elif self.spec.satisfies("%nvhpc"):
            targets.append("COMPILER=NVHPC")
            targets.append("CFLAGS_NVHPC=-mp")
        
        elif self.spec.satisfies("%arm"):
            targets.append("COMPILER=ARM")
            targets.append("CFLAGS_ARM=-fopenmp")

        elif self.spec.satisfies("%xl"):
            targets.append("COMPILER=XL")
            targets.append("CFLAGS_XL=-fopenmp")

        return targets

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.doc.tests)

        install("./neutral.omp3", prefix.bin)
        install("./problems/*", prefix.doc.tests)
