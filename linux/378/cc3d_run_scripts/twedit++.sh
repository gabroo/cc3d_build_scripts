#!/bin/sh

# necessary to enforce standard convention for numeric values specification on non-English OS
export LC_NUMERIC="C.UTF-8"


# export PREFIX_CC3D=/home/m/install_projects/3.7.6
export PREFIX_CC3D="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PYTHON_EXEC=${PREFIX_CC3D}/Python27/bin/python
export QT_XKB_CONFIG_ROOT=${PREFIX_CC3D}/Python27/lib

export PYTHON_MODULE_PATH=${PREFIX_CC3D}/pythonSetupScripts
export SWIG_LIB_INSTALL_DIR=${PREFIX_CC3D}/lib/python

export LD_LIBRARY_PATH=${PREFIX_CC3D}/lib/:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=${PREFIX_CC3D}/lib/python:$LD_LIBRARY_PATH


${PYTHON_EXEC} ${PREFIX_CC3D}/Twedit++5/twedit_plus_plus_cc3d.py $*
