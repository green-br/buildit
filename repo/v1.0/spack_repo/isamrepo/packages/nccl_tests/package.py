# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package_base import PackageBase # Or other base class

# Import the original Mpich class from the 'builtin' repository
from spack_repo.builtin.packages.nccl_tests.package import NcclTests as BuiltinNcclTests

from spack.package import *


class NcclTests(BuiltinNcclTests):
    depends_on("aws-ofi-nccl", type="run")

