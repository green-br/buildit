# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import glob

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Piclas(CMakePackage):
    """
    PICLas is a three-dimensional simulation framework for Particle-in-Cell,
    Direct Simulation Monte Carlo and other particle methods that can be
    coupled for the simulation of collisional plasma flows.
    """

    homepage = "https://piclas.readthedocs.io"
    git = "https://github.com/green-br/piclas.git"

    license("GPL-3.0-only")

    variant("eqnsysname", default="auto", description="Equation system to be solved", 
        values=(
            "auto",
            "poisson",
            "maxwell",
        ),
        multi=False
    )
    
    variant("timediscmethod", default="auto", description="Time integration method", 
        values=(
            "auto",
            "leapfrog",
            "boris-leapfrog",
            "higuera-cary",
            "RK3",
            "RK4",
            "RK14",
            "dsmc",
            "fp-flow",
            "bgk-flow",
        ), 
        multi=False
    )

    version("v3.5.0", commit="270572d6877088c5cf1a06b202aed04db2de058e" )
    version("master", commit="623d8b8bc89a90399501259b25328588982096dc" )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("mpi")
    depends_on("hdf5@1.14.0+fortran")
    depends_on("petsc@3.19.3")
    depends_on("cmake@3.17:", type="build")

    def cmake_args(self):
        args = []
        args.extend(
            [
                "-DHDF5_DIR=" + self.spec["hdf5"].prefix,
                "-DPETSC_DIR=" + self.spec["petsc"].prefix,
                "-DPETSC_ARCH=.",
            ]
        )
        if self.spec.satisfies("%gcc@10:"):
            args.append(
                self.define("CMAKE_Fortran_FLAGS", "-fallow-argument-mismatch")
            )
        if self.spec.variants["eqnsysname"].value != "auto":
            args.append("-DPICLAS_EQNSYSNAME=" + self.spec.variants["eqnsysname"].value)

        if self.spec.variants["timediscmethod"].value != "auto":
            args.append("-DPICLAS_TIMEDISCMETHOD=" + self.spec.variants["timediscmethod"].value)

        return args
