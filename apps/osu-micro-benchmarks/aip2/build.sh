#!/bin/bash
        
# Set safety options
set -eu

# Clone Spack version
git clone --depth=2 --branch=releases/v0.23 https://github.com/spack/spack.git

# Souce environment
. spack/share/spack/setup-env.sh

# Clone Buildit configuration
ln -s ../../../ ./buildit
#git clone https://github.com/isambard-sc/buildit.git

# Disable local config
export SPACK_DISABLE_LOCAL_CONFIG=true

# Create local directory "myenv" for Spack environment
spack env create -d myenv

# Activate environment
spack env activate ./myenv

# Initialise environment
spack config add -f buildit/config/aip2/v0.23/linux/compilers.yaml
spack config add -f buildit/config/aip2/v0.23/packages.yaml
spack config add view:true
spack config add concretizer:unify:true
spack config add concretizer:reuse:false

# Add local repo to environment
spack repo add ./buildit/repo/v0.23/isamrepo

# Add application
spack add osu-micro-benchmarks

# Check dependencies
spack concretize

# Install application
spack install

# Unload and reload environment (to load new view)
spack env deactivate && spack env activate ./myenv

# Check application is found
which osu_latency

# Deactivate environment
spack env deactivate


# 
