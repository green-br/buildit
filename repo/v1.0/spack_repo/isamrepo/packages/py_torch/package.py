# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_base import PackageBase # Or other base class

# Import the original Mpich class from the 'builtin' repository
from spack_repo.builtin.packages.py_torch.package import PyTorch as BuiltinPyTorch

from spack.package import *

class PyTorch(BuiltinPyTorch):
    patch(
        "https://github.com/pytorch/pytorch/commit/9d99d8879cb8a7a5ec94b04e933305b8d24ad6ac.patch?full_index=1",
        sha256="8c3a5b22d0dbda2ee45cfc2ae1da446fc20898e498003579490d4efe9241f9ee",
    )
    patch(
        "https://github.com/pytorch/kineto/commit/2ceb0a8cc04f9182b190f9214d4c6459d2021602.patch?full_index=1",
        sha256="de78bfd185c92b65a82a70183ff391a39bee700b4053711115c1a45ae87b1cac",
        working_dir="third_party/kineto",
    )
    patch(
        "https://github.com/pytorch/pytorch/commit/aaa3eb059a0294cc01c71f8e74abcebc33404e17.patch?full_index=1",
        sha256="8dcbc5cd24b4c0e4a051e2161700b485c6c598b66347e7e90a263d9319c76374",
    )


