# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_base import PackageBase # Or other base class

# Import the original Mpich class from the 'builtin' repository
from spack_repo.builtin.packages.gromacs.package import (
    Gromacs as BuiltinGromacs,
    CMakeBuilder as BuiltinCMakeBuilder
)

from spack.package import *

class Gromacs(BuiltinGromacs):
    depends_on("cmake@3.28:3", type="build", when="@2025:")

class CMakeBuilder(BuiltinCMakeBuilder):
    pass
