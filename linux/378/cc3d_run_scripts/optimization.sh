#!/bin/sh

# necessary to enforce standard convention for numeric values specification on non-English OS
export LC_NUMERIC="C.UTF-8"


# export PREFIX_CC3D=/home/m/install_projects/3.7.6
export PREFIX_CC3D="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PYTHON_EXEC=${PREFIX_CC3D}/Python27/bin/python

export CC3D_RUN_SCRIPT=${PREFIX_CC3D}/runScript.sh
export OPTIMIZATIION_PYTHON_SCRIPT=${PREFIX_CC3D}/optimization/optimization.py

export PYTHON_MODULE_PATH=${PREFIX_CC3D}/pythonSetupScripts
export SWIG_LIB_INSTALL_DIR=${PREFIX_CC3D}/lib/python

export LD_LIBRARY_PATH=${PREFIX_CC3D}/lib/:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=${PREFIX_CC3D}/lib/python:$LD_LIBRARY_PATH


${PYTHON_EXEC} ${OPTIMIZATIION_PYTHON_SCRIPT} $* --cc3d-run-script=${CC3D_RUN_SCRIPT} --clean-workdirs
# python ${PREFIX_CC3D}/Twedit++5/twedit_plus_plus_cc3d.py $*
