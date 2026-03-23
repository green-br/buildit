# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_base import PackageBase # Or other base class

from spack_repo.builtin.packages.libint.package import TUNE_VARIANTS, Libint as LibintBuiltin

from spack.package import *

class Libint(LibintBuiltin):
    
    variant(
        "mytune",
        default="none",
        multi=False,
        values=('et',),
        description="Tune libint for use with the given package",
    )

    def configure_args(self):
        config_args = super().configure_args() # Call parent method
        tune_value = self.spec.variants["mytune"].value
        if tune_value.startswith("et"):
            config_args += [
                "--enable-1body=1",
                "--enable-eri=1",
                "--enable-eri2=1",
                "--enable-eri3=1",
                "--with-max-am=6",
                "--with-opt-am=4",
            ]
        return config_args


