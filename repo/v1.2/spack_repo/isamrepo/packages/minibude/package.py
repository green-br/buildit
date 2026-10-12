# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *

class Minibude(CMakePackage):
    """implementation of the core computation of the Bristol University 
    Docking Engine (BUDE) in different HPC programming models"""

    homepage = "https://github.com/UoB-HPC/miniBUDE"
    git = "https://github.com/UoB-HPC/miniBUDE.git"

    maintainers("green-br")

    license("Apache-2.0", checked_by="green-br")

    version("main",  branch="main")

    variant(
        "model", default="serial", description="Implementation to build",
        values=("omp", "serial"), multi=False
    )

    depends_on('cxx', type='build')

    def cmake_args(self):
        args = ["--trace","-DRELEASE_FLAGS=-O3;-ffast-math"]
        #args = []
        if self.spec.variants["model"].value == "serial":
            args.append("-DMODEL=serial")
        elif self.spec.variants["model"].value == "omp":
            args.append("-DMODEL=omp")

        return args
    
    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            make("install")

        mkdirp(prefix.doc.tests)
        # Copy some test data to install location. 
        with working_dir(self.stage.source_path):
            install_tree("data", prefix.doc.tests)

