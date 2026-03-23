# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack.package import *


class CodeSaturne(AutotoolsPackage):
    """code_saturne is the free, open-source software developed primarily 
       by EDF for computational fluid dynamics (CFD) applications."""

    homepage = "https://www.code-saturne.org"
    url = "https://github.com/code-saturne/code_saturne/archive/refs/tags/v9.0.1.tar.gz"

    maintainers("green-br")

    license("GPL-2.0-or-later", checked_by="green-br")

    version("9.0.1", sha256="caaede6775b39d8066862ce6b6ea108fdad44d365f882c22f79b12084334f017")
    version("8.1.3", sha256="b228a916ad2a4d620b9f0e24296cf0d27a89fab7bdc21665a35c111549e9654a")

    # Enable or disable options.
    variant("shared", default=False, description="Build shared libraries")
    variant("gui", default=False, description="Enable the Graphical User Interface.")
    variant("long-gnum", default=True, description="Use long global numbers")
    variant("debug", default=False, description="Enable debug")

    # With or without options.
    variant("salome", default=False, description="Enable SALOME")
    variant("hdf5", default=False, description="Enable HDF5")
    variant("med", default=False, description="Enable MED")
    variant("mpi", default=False, description="Enable MPI")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("fortran", type="build")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    depends_on("mpi", when="+mpi")
    depends_on("python")

    patch("halo_fix.patch",
          sha256="8628ad70ab3e3e8ff2af71b46f06def6c2de007397300f7362711be7abc228e9",
    )

    def autoreconf(self, spec, prefix):
        autoreconf("--install", "--verbose", "--force")

    def configure_args(self):
        args = []
        args.extend(self.enable_or_disable("shared"))
        args.extend(self.enable_or_disable("gui"))
        args.extend(self.enable_or_disable("long-gnum"))
        args.extend(self.enable_or_disable("debug"))
        args.extend(self.with_or_without("salome", activation_value="prefix"))
        args.extend(self.with_or_without("hdf5", activation_value="prefix"))
        args.extend(self.with_or_without("med", activation_value="prefix"))
        args.extend(self.with_or_without("mpi", activation_value="prefix"))

        return args
