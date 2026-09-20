# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *


class Castep(MakefilePackage):
    """
    CASTEP is a leading code for calculating the
    properties of materials from first principles.
    Using density functional theory, it can simulate
    a wide range of properties of materials
    proprieties including energetics, structure at
    the atomic level, vibrational properties,
    electronic response properties etc.
    """

    homepage = "http://castep.org"
    url = f"file://{os.getcwd()}/CASTEP-25.11.tar.gz"
    manual_download = True

    version("25.1.1", sha256="af6851a973ef83bbd725f6f33ff7616dd9d589bd75cf74cd106b13c3369167f6")
    version("24.1",   sha256="97d77a4f3ce3f5c5b87e812f15a2c2cb23918acd7034c91a872b6d66ea0f7dbb")
    version("23.1",   sha256="7fba0450d3fd71586c8498ce51975bbdde923759ab298a656409280c29bf45b5")
    version("22.1.1", sha256="aca3fc2207c677561293585a4edaf233676a759c5beb8389cf938411226ef1f5")
    version("21.1.1", sha256="d909936a51dd3dff7a0847c2597175b05c8d0018d5afe416737499408914728f")
    version("20.1.1", sha256="d5e4e5503899db2820e992262df2b910227a5f50e8dd2544ffb6d7e5d6bf53e9")
    version("19.1.1", sha256="116e24904f78f7433686244134bd53d0275bede95fefb039afc907ab6b025ead")

    variant("mpi", default=True, description="Enable MPI build")
    
    # depend on compilers
    depends_on("c", type="build")
    depends_on("fortran", type="build")

    # seems to only need python
    depends_on("python", when="@24.1:")

    # distutils (removed at Python 3.12) is required at these versions
    depends_on("python@3.6:3.11", when="@:23.1")
    depends_on("py-setuptools", when="@:23.1")
    
    depends_on("rsync", type="build")
    depends_on("blas")
    depends_on("lapack")
    depends_on("fftw-api")
    depends_on("mpi", type=("build", "link", "run"), when="+mpi")

    parallel = True

    def url_version(self, version):
        split_ver = str(version).split(".")
        url_version = ".".join(split_ver[:2])
        if len(split_ver) == 3:
            url_version = url_version+split_ver[2]
        if url_version == "20.11":
            url_version = "20.11-repack1"
        return url_version

    def casteparch(self, spec):
        if spec.satisfies("platform=linux"):
            if spec.satisfies("target=x86_64:"):
                archtype="linux_x86_64"
            elif spec.satisfies("target=aarch64:"):
                archtype="linux_aarch64"
            else:
                raise InstallError("This package currently supports x86_64 and aarch64!")

        else:
            raise InstallError("This package only supports Linux!")

        # Compiler is dependent on version of Castep
        if spec.satisfies("%intel"):
            if spec.satisfies("@:19"):
                archtype=f"{archtype}_ifort19"
            elif spec.satisfies("@20:"):
                archtype=f"{archtype}_ifort"
            else:
                raise InstallError("Please add support for this version!")
        elif spec.satisfies("%gcc"): 
            if spec.satisfies("@:19"):
                archtype=f"{archtype}_gfortran9.0"
            elif spec.satisfies("@20:"):
                archtype=f"{archtype}_gfortran10"
            else:
                raise InstallError("Please add support for this version!")
        elif spec.satisfies("%nvhpc"): 
            if spec.satisfies("@25:"):
                archtype=f"{archtype}_nvfortran"
            else:
                raise InstallError("Please add support for this version!")
        elif spec.satisfies("%cce"):
            if spec.satisfies("@19:"):
                archtype=f"{archtype}_cray-XT"
            else:
                raise InstallError("Please add support for this version!")
        else:
            raise InstallError("Please add support for this compiler!")
        return archtype

    def edit(self, spec, prefix):
        archtype = self.casteparch(spec)
        platfile = FileFilter(f"obj/platforms/{archtype}.mk")
        
        if (
            spec.satisfies("@:19")
            and spec.satisfies("target=aarch64:")
        ):
            # aarch64 makefile doesnt exist at this version/
            cp = which("cp")
            cp("obj/platforms/linux_x86_64_gfortran9.0.mk",
               f"obj/platforms/{archtype}.mk")

        if spec.satisfies("%gcc"):
            if self.spec.satisfies("@:19"):
                dlmakefile = FileFilter("LibSource/dl_mg-2.0.3/platforms/castep.inc")
                dlmakefile.filter(r"MPIFLAGS = -DMPI", "MPIFLAGS = -fallow-argument-mismatch -DMPI")

                platfile.filter(r"^\s*FFLAGS_E\s*=.*", "FFLAGS_E = -fallow-argument-mismatch ")

        if spec.satisfies("%nvhpc"):
            platfile.filter(r"^FFLAGS_MODULES = ", "FFLAGS_MODULES = -Mbackslash ")
        if spec.satisfies("^cray-libsci"):
            platfile.filter(r"MATH_LIBS = \n", f"MATH_LIBS = {spec['cray-libsci'].libs.link_flags}\n")
            platfile.filter(r"MATH_LIBS = -llapack -lblas", f"MATH_LIBS = {spec['cray-libsci'].libs.link_flags}")

        platfile.filter(r"^\s*OPT_CPU\s*=.*", "OPT_CPU = ")

    @property
    def build_targets(self):
        spec = self.spec
        targetlist = [f"PWD={self.stage.source_path}"]
        archtype = self.casteparch(spec)
        
        if spec.satisfies("+mpi"):
            targetlist.append("COMMS_ARCH=mpi")
            targetlist.append(f"F90={spec['mpi'].mpifc}")
            targetlist.append(f"CC={spec['mpi'].mpicc}")
        else:
            targetlist.append(f"F90={spack_fc}")
            targetlist.append(f"CC={spack_cc}")

        targetlist.append(f"FFTLIBDIR={spec['fftw-api'].prefix.lib}")
        targetlist.append(f"MATHLIBDIR={spec['blas'].prefix.lib}")

        if spec.satisfies("^mkl"):
            targetlist.append("FFT=mkl")
            if self.spec.satisfies("@20:"):
                targetlist.append("MATHLIBS=mkl")
            else:
                targetlist.append("MATHLIBS=mkl10")

        if spec.satisfies("^openblas"):
            targetlist.append("MATHLIBS=openblas")
        elif spec.satisfies("^cray-libsci"):
            if spec.satisfies("%cce"):
                # Assumed only CCE
                targetlist.append("MATHLIBS=scilib")
            else:
                # Default patched earlier.
                targetlist.append("MATHLIBS=default")


        if spec.satisfies("^fftw"):
            targetlist.append("FFT=fftw3")
        elif spec.satisfies("^cray-fftw"):
            targetlist.append("FFT=fftw3")
        
        if not any("FFT=" in s for s in targetlist):
            raise InstallError("Castep FFT only supports certain dependencies!")
        if not any("MATHLIBS=" in s for s in targetlist):
            raise InstallError("Castep MATHLIBS only supports certain dependencies!")

        targetlist.append(f"ARCH={archtype}")

        return targetlist

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        make("install", "install-tools", *self.build_targets, "INSTALL_DIR={0}".format(prefix.bin))
