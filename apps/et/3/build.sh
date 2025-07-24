#!/bin/bash
        
# Set safety options
set -eu

# Clone Spack version
git clone --depth=2 --branch=releases/v1.0 https://github.com/spack/spack.git

# Souce environment
. spack/share/spack/setup-env.sh

# Clone Buildit configuration
#git clone https://github.com/i/buildit.git
# Use local copy
ln -s ../../../ ./buildit

# Disable local config
export SPACK_DISABLE_LOCAL_CONFIG=true

# Create local directory "myenv" for Spack environment
spack env create -d myenv

# Activate environment
spack env activate ./myenv

# Initialise environment
spack config add -f buildit/config/3/v1.0/packages.yaml
spack config add config:build_jobs:8
spack config add view:true
spack config add concretizer:unify:true
spack config add concretizer:reuse:false

# Add local repo to environment
spack repo add ./buildit/repo/v1.0/spack_repo/isamrepo

# Add application
spack add et

# Check dependencies
spack concretize -f

# Install application
spack install

# Unload and reload environment (to load new view)
spack env deactivate && spack env activate ./myenv

# Check application is found
which eT_launch.py

# Deactivate
spack env deactivate
