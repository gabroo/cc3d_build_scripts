#!/usr/bin/env bash

# this is your home directory - change it as needed
export HOME_DIR=/N/u/mswat/BigRed2

# cc3d_377 is the name of the python env that we create using this command: conda create -n cc3d_377 python=2.7
export PYTHON_ROOT=${HOME_DIR}/.conda_envs/cc3d_377

export INSTALL_PREFIX=${WORK_DIR}/${VTK_CORE_NAME}_install




export INSTALL_PREFIX=${WORK_DIR}/${VTK_CORE_NAME}_install


cp -R ${INSTALL_PREFIX}/bin ${PYTHON_ROOT}....
cp -R ${INSTALL_PREFIX}/include ${PYTHON_ROOT}....
cp -R ${INSTALL_PREFIX}/lib ${PYTHON_ROOT}....
cp -R ${INSTALL_PREFIX}/python/site-packages ${PYTHON_ROOT}/lib/python2.7
