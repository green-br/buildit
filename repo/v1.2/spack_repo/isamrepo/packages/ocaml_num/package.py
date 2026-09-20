# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *


class OcamlNum(MakefilePackage):
    """The legacy Num library for arbitrary-precision integer and rational
       arithmetic that used to be part of the OCaml core distribution"""

    homepage = "https://github.com/ocaml/num"
    url = "https://github.com/ocaml/num/archive/v1.5.tar.gz"
    git = "https://github.com/ocaml/num.git"

    maintainers("green-br")

    license("LGPL-2.0-only")

    version("develop", branch="master")

    depends_on("c", type="build")  # generated

    # Dependency demands ocamlbuild
    depends_on("ocaml")
    depends_on("ocamlbuild")

    def install(self, spec, prefix):
        make("install", "DESTDIR=%s" % prefix)
