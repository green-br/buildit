#!/bin/bash
        
# Set safety options
set -eu

# Find expected common config
MYSELF=`readlink -f $0`
MYDIR=`dirname $MYSELF`
SYSTEM_NAME=`basename $(dirname $MYSELF)`
SOFTWARE_NAME=`basename $(dirname $MYDIR)`
CONFIG=`readlink -f $MYDIR/../../../config/$SYSTEM_NAME`
ENV_BASENAME=isambench_${SYSTEM_NAME}_${SOFTWARE_NAME}
MY_SPACK=`readlink -f $MYDIR/../../../spack`


# Check for Spack location (maybe download a fixed version?)
[ ! -d $MY_SPACK ] && echo "ERROR: Please install spack in $MY_SPACK" && exit 1
        
# Load Spack environment
. $MY_SPACK/share/spack/setup-env.sh

echo "INFO: Building $SOFTWARE_NAME for $SYSTEM_NAME"

# Create spack.yml for environment
# cce@17.0.0 not supported in CUDA.
# gcc@12.3.0 seems to work
for comp in gcc@12.3.0 nvhpc@24.9
do
        # Remove characters Spack do not support.
        comppath=${comp//@/-}
        comppath=${comppath//./-}_openmpi
        cat > spack.yaml<<EOF
spack:
  include:
    - $CONFIG/linux/compilers.yaml
    - $CONFIG/packages.yaml
  view: true
  concretizer:
    unify: true
    reuse: false
  specs:
    - osu-micro-benchmarks %${comp} +cuda ^openmpi

EOF
        # Create an environment
        if ! spack env create ${ENV_BASENAME}_${comppath} spack.yaml
        then
                echo "INFO: Removing env" && spack env remove -y ${ENV_BASENAME}_${comppath}
                echo "INFO: Creating env" && spack env create ${ENV_BASENAME}_${comppath} spack.yaml
fi

        # Activate environment
        spack env activate ${ENV_BASENAME}_${comppath}
        spack concretize
        spack install
done

# Create spack.yml for environment
# cce@17.0.0 not supported in CUDA.
# gcc@12.3.0 seems to work
for comp in gcc@12.3.0 nvhpc@24.9
do
        # Remove characters Spack do not support.
        comppath=${comp//@/-}
        comppath=${comppath//./-}_mpich
        cat > spack.yaml<<EOF
spack:
  include:
    - $CONFIG/linux/compilers.yaml
    - $CONFIG/packages.yaml
  view: true
  concretizer:
    unify: true
    reuse: false
  specs:
    - osu-micro-benchmarks %${comp} +cuda ^mpich

EOF
        # Create an environment
        if ! spack env create ${ENV_BASENAME}_${comppath} spack.yaml
        then
                echo "INFO: Removing env" && spack env remove -y ${ENV_BASENAME}_${comppath}
                echo "INFO: Creating env" && spack env create ${ENV_BASENAME}_${comppath} spack.yaml
fi

        # Activate environment
        spack env activate ${ENV_BASENAME}_${comppath}
        spack concretize
        spack install
done
