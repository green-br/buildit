# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package_base import PackageBase # Or other base class

# Import the original Mpich class from the 'builtin' repository
from spack_repo.builtin.packages.nccl_tests.package import NcclTests as BuiltinNcclTests

from spack.package import *


class NcclTests(BuiltinNcclTests):
    version("2.17.6", sha256="38974e70342150ede0e3fb8fd24bfe60ccbde90fa20241716ba8bb338e6b61a0")
    depends_on("aws-ofi-nccl", type="run")

