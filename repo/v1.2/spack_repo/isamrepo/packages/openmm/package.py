# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


# Import the original Mpich class from the 'builtin' repository
from spack_repo.builtin.packages.openmm.package import Openmm as BuiltinOpenmm

from spack.package import *

class Openmm(BuiltinOpenmm):
    version("8.1.2", sha256="afc888a4e46486d8d68dac4d403e2b0b28f51b95e52e821e34c38e8b428e040e")
    
    def patch(self):
        super().patch()  # Call parent method
        install_string = f'set(PYTHON_SETUP_COMMAND "install")'

        filter_file(
            r"set\(PYTHON_SETUP_COMMAND \"install.*",
            install_string,
            "wrappers/python/CMakeLists.txt",
        )
        filter_file(
            r"HWCAP_NEON",
            "HWCAP_ASIMD",
            "openmmapi/include/openmm/internal/vectorize_neon.h",
        )

