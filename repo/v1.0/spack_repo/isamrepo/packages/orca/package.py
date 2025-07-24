# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import platform

from spack_repo.builtin.build_systems.generic import Package

from spack.package import *

_versions = {
    "6.0.1": {
        "Linux-aarch64": "0699cbccb6dbee66e14e69c4bb1300b35820b4222afdd7371e50aa23fe28be48",
        "Linux-x86_64": "5e9b49588375e0ce5bc32767127cc725f5425917804042cdecdfd5c6b965ef61",
    },
}

class Orca(Package):
    """An ab initio, DFT and semiempirical SCF-MO package

    Note: Orca is licensed software. You will need to create an account
    on the Orca homepage and download Orca yourself. Spack will search
    your current directory for the download file. Alternatively, add this
    file to a mirror so that Spack can find it. For instructions on how to
    set up a mirror, see https://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "https://cec.mpg.de"
    maintainers("snehring")
    manual_download = True

    license("LGPL-2.1-or-later")
    
    for ver, packages in _versions.items():
        key = "{0}-{1}".format(platform.system(), platform.machine())
        sha_val = packages.get(key)
        if sha_val:
            version(ver, sha256=sha_val, deprecated=packages.get("deprecated", False))
    
    depends_on("libevent", type="run")
    depends_on("libpciaccess", type="run")

    # Map Orca version with the required OpenMPI version
    # OpenMPI@4.1.1 has issues in pmix environments, hence 4.1.2 here
    openmpi_versions = {
        "6.0.1": "4.1.8",
    }

    for orca_version, openmpi_version in openmpi_versions.items():
        depends_on(
            "openmpi@{0}".format(openmpi_version), type="run", when="@{0}".format(orca_version)
        )

    def url_for_version(self, version):
        openmpi_version = self.openmpi_versions[version.string].replace(".", "")
        if openmpi_version == "412":
            openmpi_version = "411"
        ver_parts = version.string.split("-")
        ver_underscored = ver_parts[-1].replace(".", "_")
        features = ver_parts[:-1] + ["shared"]
        feature_text = "_".join(features)
        orca_arch = "linux_x86-64"
        if platform.system() == "Linux" and platform.machine() == "aarch64":
            orca_arch = "linux_arm64"
        return f"file://{os.getcwd()}/orca_{ver_underscored}_{orca_arch}_{feature_text}_openmpi{openmpi_version}.tar.xz"

    def install(self, spec, prefix):
        mkdirp(prefix.bin)

        install_tree(".", prefix.bin)

        # Check "mpirun" usability when building against OpenMPI
        # with Slurm scheduler and add a "mpirun" wrapper that
        # calls "srun" if need be
        if "^openmpi ~legacylaunchers schedulers=slurm" in self.spec:
            mpirun_srun = join_path(os.path.dirname(__file__), "mpirun_srun.sh")
            install(mpirun_srun, prefix.bin.mpirun)

    def setup_run_environment(self, env):
        env.prepend_path("LD_LIBRARY_PATH", self.prefix.bin)
        env.prepend_path("LD_LIBRARY_PATH", self.spec["libevent"].prefix.lib)
        env.prepend_path("LD_LIBRARY_PATH", self.spec["libpciaccess"].prefix.lib)
        env.prepend_path("LD_LIBRARY_PATH", self.spec["openmpi"].prefix.lib)
