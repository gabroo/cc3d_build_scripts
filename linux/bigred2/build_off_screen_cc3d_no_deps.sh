
#!/usr/bin/env bash

# tested on RedHat 7.5 with VTK-6.3.0
# make sure all entries ofr libraries include dirs are correct and that the files exist
# we assume you are using python distribution layout from miniconda2 on linux

# example command line
# vtk-offscreen.sh /home/m/Downloads/VTK-6.3.0.tar.gz /home/m/Downloads/VTK-6.3.0-offscreen
export HOME_DIR=/N/u/mswat/BigRed2
export CC3D_SOURCE_PATH=${HOME_DIR}/CC3D_GIT/CompuCell3D
export INSTALL_PREFIX=${HOME_DIR}/cc3d_379_offscreen

export WORK_DIR=${HOME_DIR}/cc3d_379_offscreen_build

# this is the same python env we created for vtk  ,and this is where vtk resides after installation
export PYTHON_ROOT=${HOME_DIR}/.conda_envs/cc3d_377

export PYTHON_LIB=${PYTHON_ROOT}/lib/libpython2.7.so
export PYTHON_INCLUDE=${PYTHON_ROOT}/include/python2.7
export PYTHON_EXEC=${PYTHON_ROOT}/bin/python
export VTK_DIR=${PYTHON_ROOT}/lib/cmake/vtk-6.3


# important set of CRay linux settings that enable dynamic linking on Cray linux
#https://github.com/LLNL/GOTCHA/issues/41
export XTPE_LINK_TYPE=dynamic
export CRAYPE_LINK_TYPE=dynamic

# this will force the use of standard gcc compiler on BigRed
export CXX=
export CC=

mkdir ${WORK_DIR}
# setup dirs
cd ${WORK_DIR}

# configure/generate vtk makefiles
cmake \
 -G "Unix Makefiles" \
 -DCMAKE_BUILD_TYPE:STRING=Release \
 -DNO_OPENCL:BOOLEAN=ON \
 -DCMAKE_INSTALL_PREFIX:PATH=${INSTALL_PREFIX} \
 -DCOMPUCELL3D_A_MAJOR_VERSION:STRING=3 \
 -DCOMPUCELL3D_A_MINOR_VERSION:STRING=7 \
 -DCOMPUCELL3D_A_BUILD_VERSION:STRING=9 \
 -DPYTHON_EXECUTABLE=${PYTHON_EXEC} \
 -DPYTHON_INCLUDE_DIR=${PYTHON_INCLUDE} \
 -DPYTHON_LIBRARY=${PYTHON_LIB} \
 -DVTK_DIR==${VTK_DIR} \
 -DPYQT_VERSION:STRING=5 \
 ${CC3D_SOURCE_PATH}


# compilation

cd ${WORK_DIR}
make -j 2
make install


