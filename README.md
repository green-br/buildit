# buildit

This is a repository to contain examples of using build tools on various systems.

Focusses initially on Spack.

# Spack

First get a copy of this repo.

```
$ git clone https://github.com/green-br/buildit.git
$ cd buildit
```

Install Spack as suggested on https://spack.readthedocs.io 

```
$ git clone -c feature.manyFiles=true --depth=2 https://github.com/spack/spack.git
```

Then add to your shell, for example:

```
$ . spack/share/spack/setup-env.sh
```

As an example for osu-micro-benchmarks on Isambard-AI checkout this repository

```
$ cd apps/osu-micro-benchmarks/aip1
$ ./build.sh
```

This will use an Spack environment which can be activated to run the software.

The `config` directory has the Spack config that is included by the build script.

 
