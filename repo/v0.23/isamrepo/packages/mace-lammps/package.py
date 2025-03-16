# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack.package import *


class MaceLammps(CMakePackage):
    """
    MACE provides fast and accurate machine learning interatomic 
    potentials with higher order equivariant message passing with
    interface to LAMMPS which stands for Large-scale Atomic/Molecular Massively
    Parallel Simulator. 
    """

    homepage = "https://mace-docs.readthedocs.io"
    git = "https://github.com/ACEsuit/lammps"

    license("GPL-2.0-only")

    version("develop", commit="f51963aada27c5df4a87a37faec5a4125d0f2e82")
    
    depends_on("cxx", type="build")

    depends_on("mpi")
    depends_on("py-torch")
    
    root_cmakelists_dir = "cmake"

    def cmake_args(self):
        args = [
            self.define("CMAKE_CXX_STANDARD", 17),
            self.define("CMAKE_CXX_STANDARD_REQUIRED", "ON"),
            self.define("BUILD_MPI", "ON"),
            self.define("BUILD_OMP", "ON"),
            self.define("PKG_OPENMP", "ON"),
            self.define("PKG_ML-MACE", "ON"),
        ]

        return args

