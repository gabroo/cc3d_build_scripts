VTK Compilation in the offscreen mode
=====================================

To compile VTK in the off-screen mode you need to first make sure you have OSMesa library compiled
. This is the hardest part of the job. When you compile mesa library you need to
make sure you have the following libraries:

**libGL.so** and **libOSMesa.so**. other libraries you may get during compilation
include:

libglapi.so      libGLESv2.so
libgbm.so  libGLESv1_CM.so  libGL.so


Compiling Mesa with off screen rendering capabilities
-----------------------------------------------------

We have used Mesa17.10 version of Mesa libraries

Mesa library can be obtained by visiting

https://www.mesa3d.org/

They have also nice introductory installation tutorials:

https://www.mesa3d.org/install.html

Before proceeding we may also explore the following resource:

https://www.paraview.org/Wiki/ParaView_And_Mesa_3D

The trick with compiling mesa library is to first install its core dependencies:
notably llvm and then run configure script. It is very likely that the configure script
will complain multiple times about missing libraries. You have not take note what libraries are
missing and install them (easiest thing here is to use linux package manager - either yum or apt)

The following list explains how we built mesa on RedHat 7.5. First unpack
downloaded mesa package. In our case we we placed it in */home/m/Downloads/mesa-17.3.9*

so

.. code-block:: console

    cd /home/m/Downloads/mesa-17.3.9

Next we run *configure*


.. code-block:: console

    ./configure --prefix=/home/m/mesa --enable-llvm --enable-osmesa

note, that we need **llvm** at this point. You may install llvm as outlined in
https://www.paraview.org/Wiki/ParaView_And_Mesa_3D or you may
use package manager. We ran the following command:

.. code-block:: console

    yum install mesa-private-llvm-devel

We also had to soft-link */usr/bin/mesa-private-llvm-config-64* to */usr/bin/llvm-config*

You may compile llvm manually and then llvm-config will be created without name-mangling

After installing **llvm** we stil got several compaints about missing libraries. We fixed them
by running the following commands:

.. code-block:: console

    yum install zlib-devel
    yum install libdrm-devel
    yum install libXext-devel
    yum install libXdamage-devel
    yum install libxshmfence-devel
    yum install expat-devel

After successfully getting through *configure* you compile mesa

.. code-block:: console
    make -j 2
    make install

Once Mesa libraries are installed we can start installation of VTK with the off-screen rendering support
**Important** when you compile VTK in the off-screen mode you may not beable
to render images on the screen. This means that your rendering can be only written to a file


VTK compilation
---------------

One resource you may explore before proceeding further is this useful blog post

https://patricksnape.github.io/2014/offscreen_rendering/


We developed a script that compiles VTK in the offscreen mode the key thing is to
make sure that all libraries, paths, include dirs etc listed in the script exist on your
machine. If you have libraries in different locations you NEED TO edit the script
to reflect those differences.

After that you simply run the script and it will compile VTK and place all the files
in your miniconda environment :

.. code-block:: console

    ./vtk-offscreen.sh

At that stage you are ready to build CC3D using build-no-x.py script
Note that you will not be able to use this distribution of CC3D int he
interactive mode with the GUI. This version will be for off-screen, , mostly cluster
use only


For completness we include the content of the script below:

.. code-block:: bash

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



