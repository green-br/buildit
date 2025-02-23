# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import glob

from spack.package import *


class Hopr(CMakePackage):
    """
    HOPR is an open-source tool for the generation of three-dimensional unstructured high-order meshes.
    """

    homepage = "https://hopr.readthedocs.io"
    git = "https://github.com/hopr-framework/hopr.git"

    license("GPL-3.0-only")

    version("master", commit="e54eddedc613f1cd32439b55a7e2f428ceb116ce", get_full_repo=True)

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("mpi")
    depends_on("hdf5@1.12.0+fortran")
    depends_on("lapack")
    # CGNS at 3.4.1 has CMake issues due to h5dump
    # See: https://github.com/CGNS/CGNS/pull/215
    #depends_on("cgns@3.4.1+fortran")
    depends_on("cmake@3.17:", type="build")

    def cmake_args(self):
        args = []
        args.extend(
            [
                "-DHDF5_DIR=" + self.spec["hdf5"].prefix,
                "-DLIBS_BUILD_HDF5=OFF",
                "-DLIBS_BUILD_CGNS=OFF",
                "-DLIBS_USE_CGNS=OFF",
                "-DCMAKE_EXE_LINKER_FLAGS=" + self.spec['lapack'].libs.ld_flags
            ]
        )
        return args
