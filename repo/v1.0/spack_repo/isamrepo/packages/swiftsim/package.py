# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_base import PackageBase # Or other base class

# Import the original Mpich class from the 'builtin' repository
from spack_repo.builtin.packages.swiftsim.package import Swiftsim as BuiltinSwiftsim

from spack.package import *

class Swiftsim(BuiltinSwiftsim):
    version("master", branch="master")
    depends_on("fftw-api@3.3:")

    def configure_args(self):
        return [
            "--enable-mpi" if "+mpi" in self.spec else "--disable-mpi",
            "--with-metis={0}".format(self.spec["metis"].prefix),
            "--with-fftw={0}".format(self.spec["fftw-api"].prefix),
            "--disable-dependency-tracking",
            "--enable-optimization",
            "--enable-compiler-warnings=yes",
            "--disable-vec",
        ]
