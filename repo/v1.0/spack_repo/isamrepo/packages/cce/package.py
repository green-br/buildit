# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_base import PackageBase # Or other base class

# Import the original Mpich class from the 'builtin' repository
from spack_repo.builtin.packages.cce.package import Cce as BuiltinCce

from spack.package import *

# Archspec used by Spack for default compiler options
# do no support Cray Compiler so need to report "clang".

class Cce(BuiltinCce):
    def archspec_name(self):
        return "clang"
