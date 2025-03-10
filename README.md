# buildit

This is a repository to contain examples of using build tools on various systems.

Focusses initially on Spack.

# Spack

As an example for osu-micro-benchmarks on Isambard-AI checkout this repository

```bash
$ cd apps/osu-micro-benchmarks/aip1
$ ./build.sh
```

This will use an Spack environment which can be activated to run the software.

The `config` directory has the Spack config that is included by the build script.

The `repo` directory contains Spack packages which were either modified from existing packages or completely new.

`build.sh` downloads its own version of Spack.  If an existing version of Spack is available the script can be modified to use the existing version.  This can help with sharing already installed dependencies between different packages.

# Reframe

ReFrame is a powerful framework for writing system regression tests and benchmarks, specifically targeted to HPC systems.  An initial configuration to use Reframe is provided.

```bash
$ cd reframe
$ python3 -m venv venv
$ . venv/bin/activate
$ pip install -U pip
$ pip install reframe-hpc
$ git clone --depth=2 --branch=releases/v0.23 https://github.com/spack/spack.git
$ . spack/share/spack-env.sh
```
 
Modify `config/i3.py` to point to where buildit repository was cloned.

Isambard 3 configuration is currently provided, an example of building bzip2 is provided as a sanity check.

```bash
$ reframe -C config/i3.py -c config/spack_test.py -r
```

