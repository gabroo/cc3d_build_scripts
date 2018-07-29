#!/bin/sh
current_directory=$(pwd)


# necessary to enforce standard convention for numeric values specification on non-English OS
export LC_NUMERIC="C.UTF-8"


# export PREFIX_CC3D=/home/m/install_projects/3.7.6
export PREFIX_CC3D="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export PYTHON_EXEC=${PREFIX_CC3D}/Python27/bin/python

export MAX_NUMBER_OF_CONSECUTIVE_RUNS=50

cd $PREFIX_CC3D
#export LD_LIBRARY_PATH=:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=${PREFIX_CC3D}/lib/:$LD_LIBRARY_PATH

export COMPUCELL3D_PLUGIN_PATH=${PREFIX_CC3D}/lib/CompuCell3DPlugins
export COMPUCELL3D_STEPPABLE_PATH=${PREFIX_CC3D}/lib/CompuCell3DSteppables
export LD_LIBRARY_PATH=${PREFIX_CC3D}/lib/python:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=${COMPUCELL3D_PLUGIN_PATH}:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=${COMPUCELL3D_STEPPABLE_PATH}:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=:$LD_LIBRARY_PATH
export SWIG_LIB_INSTALL_DIR=${PREFIX_CC3D}/lib/python
export PYTHON_MODULE_PATH=${PREFIX_CC3D}/pythonSetupScripts


export COMPUCELL3D_MAJOR_VERSION=3
export COMPUCELL3D_MINOR_VERSION=7
export COMPUCELL3D_BUILD_VERSION=6

export SOSLIB_PATH=${PREFIX_CC3D}/examplesSoslib

echo "CompuCell3D - version $COMPUCELL3D_MAJOR_VERSION.$COMPUCELL3D_MINOR_VERSION.$COMPUCELL3D_BUILD_VERSION"

export exit_code=0
${PYTHON_EXEC} ${PREFIX_CC3D}/player5/compucell3d.pyw $* --currentDir=${current_directory}
exit_code=$?

cd ${current_directory}
exit ${exit_code}
