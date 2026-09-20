from spack.package_base import PackageBase

from spack_repo.builtin.packages.osu_micro_benchmarks.package import OsuMicroBenchmarks as BuiltinOsuMicroBenchmarks

from spack.package import *


class OsuMicroBenchmarks(BuiltinOsuMicroBenchmarks):
    version("7.5.2", sha256="618de3d0b1122f73a9229177d2da1e5cd62e431190580cb915f2605849cbbbdc")

