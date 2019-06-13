#!/usr/bin/env bash

# tested on RedHat 7.5 with VTK-6.3.0
# make sure all entries ofr libraries include dirs are correct and that the files exist
# we assume you are using python distribution layout from miniconda2 on linux

# example command line
# vtk-offscreen.sh /home/m/Downloads/VTK-6.3.0.tar.gz /home/m/Downloads/VTK-6.3.0-offscreen
export VTK_CORE_NAME=VTK-6.3.0

export VTK_TAR_GZ=/home/m/Downloads/${VTK_CORE_NAME}tar.gz
export WORK_DIR=/home/m/Downloads/${VTK_CORE_NAME}-offscreen

# note: I am using "demo_python" python environment in the miniconda python

export MESA_DIR=/home/m/mesa
export MESA_INCLUDE=${MESA_DIR}/include
export MESA_GL=${MESA_DIR}/lib/libGL.so
export MESA_OSMESA=${MESA_DIR}/lib/libOSMesa.so


export PYTHON_ROOT=/home/m/miniconda2/envs/demo_python

export PYTHON_LIB=${PYTHON_ROOT}/lib/libpython2.7.so
export PYTHON_INCLUDE=${PYTHON_ROOT}/include/python2.7
export PYTHON_EXEC=${PYTHON_ROOT}/bin/python2

export INSTALL_PREFIX=/home/m/vtk-6.3.0-off-screen
export CMAKE_BUILD_TYPE=RelWithDebInfo

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

# installing into miniconda environment  python

cp -R ${INSTALL_PREFIX}/bin ${PYTHON_ROOT}
cp -R ${INSTALL_PREFIX}/include ${PYTHON_ROOT}
cp -R ${INSTALL_PREFIX}/lib ${PYTHON_ROOT}
cp -R ${INSTALL_PREFIX}/python/site-packages ${PYTHON_ROOT}/lib/python2.7
cp ${MESA_DIR}/lib/lib* ${PYTHON_ROOT}/lib

