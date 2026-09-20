# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.packages.aws_ofi_nccl.package import AwsOfiNccl as BuiltinAwsOfiNccl

from spack.package import *


class AwsOfiNccl(BuiltinAwsOfiNccl):
    version("1.18.0", sha256="12fd67f05872600c485d74b8e3c3a640d063322371170f3a9c17d67a5a2ca681")

