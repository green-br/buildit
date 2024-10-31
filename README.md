# buildit

This is a repository to contain examples of using build tools on various systems.

Focusses initially on Spack.

# Spack

Install Spack as suggested on https://spack.readthedocs.io 

For example:

```
$ git clone -c feature.manyFiles=true --depth=2 https://github.com/spack/spack.git
```

Add to your shell, for example:

```
$ . spack/share/spack/setup-env.sh
```

As an example for osu-micro-benchmarks on Isambard-AI checkout this repository

```
$ git clone https://github.com/green-br/buildit.git
$ cd buildit/apps/osu-micro-benchmarks/i-ai
$ ./build.sh
```

This will use an Spack environment which can be activated to run the software.

The `config` directory has the Spack config that is included by the build script.

 
