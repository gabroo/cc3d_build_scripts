#!/usr/bin/env bash

# this is your home directory - change it as needed
export HOME_DIR=/N/u/mswat/BigRed2

# cc3d_377 is the name of the python env that we create using this command: conda create -n cc3d_377 python=2.7
export PYTHON_ROOT=${HOME_DIR}/.conda_envs/cc3d_377

# those are python libr, exec and includes that VTK needs - note, they point to cc3d_377 python env
export PYTHON_LIB=${PYTHON_ROOT}/lib/libpython2.7.so
export PYTHON_INCLUDE=${PYTHON_ROOT}/include/python2.7
export PYTHON_EXEC=${PYTHON_ROOT}/bin/python

# we assume that vtk version we will use is 6.3.0 - other versions may require different set of settings in the offscreen mode
export VTK_CORE_NAME=VTK-6.3.0
export VTK_TAR_GZ=${HOME_DIR}/Downloads/${VTK_CORE_NAME}.tar.gz

export WORK_DIR=${HOME_DIR}/Downloads/${VTK_CORE_NAME}-offscreen

# this specifies where vtk will be initially installed
export INSTALL_PREFIX=${WORK_DIR}/${VTK_CORE_NAME}_install

export CMAKE_BUILD_TYPE=RelWithDebInfo


# this is a super-important thing that points to the mesa library installed on BigRed2
# you also need to make sure you use module load mesa
export MESA_DIR=/N/soft/cle4/mesa/gnu/7.4.1
export MESA_INCLUDE=${MESA_DIR}/include
export MESA_GL=${MESA_DIR}/lib/libGL.so
export MESA_OSMESA=${MESA_DIR}/lib/libOSMesa.so

# important set of CRay linux settings that enable dynamic linking on Cray linux
#https://github.com/LLNL/GOTCHA/issues/41
export XTPE_LINK_TYPE=dynamic
export CRAYPE_LINK_TYPE=dynamic

# this will force the use of standard gcc compiler on BigRed
export CXX=
export CC=

# =============== COMPILATION SECTION =======================
# unpack tar.gz to workdir
mkdir ${WORK_DIR}
tar -zxvf ${VTK_TAR_GZ} -C ${WORK_DIR}

# setup dirs
mkdir ${WORK_DIR}/${VTK_CORE_NAME}_build


cd ${WORK_DIR}/${VTK_CORE_NAME}_build

# configure/generate vtk makefiles
cmake \
 -DBUILD_SHARED_LIBS=ON \
 -DVTK_WRAP_PYTHON=ON \
 -DVTK_USE_X=OFF \
 -DOPENGL_INCLUDE_DIR=${MESA_INCLUDE} \
 -DOPENGL_gl_LIBRARY=${MESA_GL}/ \
 -DVTK_OPENGL_HAS_OSMESA=ON \
 -DOSMESA_INCLUDE_DIR=${MESA_INCLUDE} \
 -DOSMESA_LIBRARY=${MESA_OSMESA} \
 -DVTK_WRAP_PYTHON=ON \
 -DPYTHON_EXECUTABLE=${PYTHON_EXEC} \
 -DPYTHON_INCLUDE_DIR=${PYTHON_INCLUDE} \
 -DPYTHON_LIBRARY=${PYTHON_LIB} \
 -DVTK_INSTALL_PYTHON_MODULE_DIR=${INSTALL_PREFIX}/python/site-packages \
 -DCMAKE_INSTALL_PREFIX=${INSTALL_PREFIX} \
 -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE} \
 ${WORK_DIR}/${VTK_CORE_NAME}

# compilation

cd ${WORK_DIR}/${VTK_CORE_NAME}_build
make -j 2
make install

# final installation into  python env
cp -R ${INSTALL_PREFIX}/bin ${PYTHON_ROOT}....
cp -R ${INSTALL_PREFIX}/include ${PYTHON_ROOT}....
cp -R ${INSTALL_PREFIX}/lib ${PYTHON_ROOT}....
cp -R ${INSTALL_PREFIX}/python/site-packages ${PYTHON_ROOT}/lib/python2.7