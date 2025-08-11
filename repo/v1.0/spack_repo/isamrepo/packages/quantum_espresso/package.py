# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_base import PackageBase # Or other base class

# Import the original Mpich class from the 'builtin' repository
from spack_repo.builtin.packages.quantum_espresso.package import QuantumEspresso as BuiltinQuantumEspresso
from spack_repo.builtin.packages.quantum_espresso.package import CMakeBuilder as BuiltinCMakeBuilder
from spack_repo.builtin.packages.quantum_espresso.package import GenericBuilder as BuiltinGenericBuilder

from spack.package import *

class QuantumEspresso(BuiltinQuantumEspresso):
    pass

class CMakeBuilder(BuiltinCMakeBuilder):
 
    def cmake_args(self):
        cmake_args = super().cmake_args() # Call parent method
        spec = self.spec
        if "^cray-libsci" in spec:
            cmake_args.append(self.define("SCALAPACK_LIBRARIES", spec["scalapack"].libs.joined(";")))
            cmake_args.append(self.define("BLAS_LIBRARIES", spec["blas"].libs.joined(";")))
            cmake_args.append(self.define("LAPACK_LIBRARIES", spec["lapack"].libs.joined(";")))
            # Up to q-e@7.1 set BLA_VENDOR to All to force detection of vanilla scalapack
            if spec.satisfies("@:7.1"):
                cmake_args.append(self.define("BLA_VENDOR", "All"))
        return cmake_args

class GenericBuilder(BuiltinGenericBuilder):
    pass
