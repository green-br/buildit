# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import glob

from spack.package import *


class Tealeaf(MakefilePackage):
    """Proxy Application. TeaLeaf is a mini-app that solves
    the linear heat conduction equation on a spatially decomposed
    regularly grid using a 5 point stencil with implicit solvers.
    """

    homepage = "https://uk-mac.github.io/TeaLeaf/"
    url = "https://downloads.mantevo.org/releaseTarballs/miniapps/TeaLeaf/TeaLeaf-1.0.tar.gz"
    git = "https://github.com/UK-MAC/TeaLeaf.git"

    tags = ["proxy-app"]

    license("LGPL-3.0-only")

    version("1.0", sha256="e11799d1a3fbe76041333ba98858043b225c5d65221df8c600479bc55e7197ce")
    version("master", branch="master", submodules=True)

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("mpi")

    def edit(self, spec, prefix):
        filter_file("-march=native", "", join_path("TeaLeaf_ref", "Makefile"))

    @property
    def build_targets(self):
        targets = [
            "--directory=TeaLeaf_ref",
            "MPI_COMPILER={0}".format(self.spec["mpi"].mpifc),
            "C_MPI_COMPILER={0}".format(self.spec["mpi"].mpicc),
            "FLAGS_GNU=-O3 -funroll-loops -cpp -ffree-line-length-none",
            "CFLAGS_GNU=-O3 -funroll-loops",
            "OMP_CRAY=-fopenmp",
            "FLAGS_CRAY=-O3 -e Z",
            "CFLAGS_CRAY=-O3",
            "OMP_ARM=-fopenmp",
            "FLAGS_ARM=-O3 -cpp",
            "CFLAGS_ARM=-O3",
            "OMP_NVHPC=-fopenmp",
            "FLAGS_NVHPC=-O3 -cpp",
            "CFLAGS_NVHPC=-O3",
        ]

        if "%gcc" in self.spec:
            targets.append("COMPILER=GNU")
        elif "%cce" in self.spec:
            targets.append("COMPILER=CRAY")
        elif "%intel" in self.spec:
            targets.append("COMPILER=INTEL")
        elif "%pgi" in self.spec:
            targets.append("COMPILER=PGI")
        elif "%xl" in self.spec:
            targets.append("COMPILER=XL")
        elif "%arm" in self.spec:
            targets.append("COMPILER=ARM")
        elif "%nvhpc" in self.spec:
            targets.append("COMPILER=NVHPC")


        return targets

    def install(self, spec, prefix):
        # Manual Installation
        mkdirp(prefix.bin)
        mkdirp(prefix.doc.tests)

        install("README.md", prefix.doc)
        install("TeaLeaf_ref/tea_leaf", prefix.bin)
        install("TeaLeaf_ref/tea.in", prefix.bin)

        for f in glob.glob("TeaLeaf_ref/*.in"):
            install(f, prefix.doc.tests)
        for f in glob.glob("TeaLeaf_ref/Benchmarks/*.in"):
            install(f, prefix.doc.tests)
       
