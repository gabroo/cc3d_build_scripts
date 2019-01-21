Building CC3D On Big Red2:
=========================

BigRed2 uses Cray linux - and this ia major reason why e.g. many packages from standard anaconda distribution will not work there
For example vtk, PyQt, matplotlib that work out-of-the-box on many standard linux distributions need to be essentially recompiled
on Cray Linux.

Here is  a link that goes deeper into this discussion:

https://github.com/ContinuumIO/anaconda-issues/issues/1757

Therefore to  compile CC3D on BigRed2 you need to start from compiling VTK in the off-screen mode. Since you are not
displaying images on the worker nodes but you want to have screenshots output you will need this special compilation of
vtk. If you need "regular" compilation of vtk you can also do this in a very similar fashion to the way we describe below
The key idea here is manual specification of mesa library on BigRed. Fortunately mesa linrary installed there seems to be working
OK.

First thing is to load appropriate modules - some of those commands we will put later in the startup script so that you do not
need to enter them manually each time you compile or run things on BigRed2 (see example ``big_red_environment_setup.sh``
. You may include it in your .bashrc script on bigred2 to avoid manual loading of the modules)

.. code-block:: console

    export LFLAGS=-L/N/soft/cle4/mesa/gnu/7.4.1/lib
    module unload python
    module load anaconda2/4.2.0
    module load git/2.17.0
    module load mesa


The ``LFLAGS`` setting is necessary to properly link VTK during compilation


Keep in mind, that even though anacnoda is installed and it has vtk /pyqt5 they are not functional on BigRed2. You need
to create your own python environment and install vtk there. since we arewill not be using cc3d in the GUI mode we do not need
PyQt5 and this will simplify things.

Creating your  new python virtual environment aka conda environment:

.. code-block:: console

  conda create -n cc3d_377 python=2.7

After the environment ``cc3d_377`` is created we will activate it. BTW you can call this environment whatever you want. Just
Keep the names meaningful to you


.. code-block:: console

  source activate cc3d_377

Let's install numpy inside this environment because we will need it for the CC3D compilation:

.. code-block:: console

    conda install numpy


Now we will compile vtk in the off-screen mode. I will be using a script that will carry out the compilation.
First we go to the ``Download`` folder and download VTK-6.3.0

.. code-block:: console

    cd ~/Downloads
    wget https://www.vtk.org/files/release/6.3/VTK-6.3.0.tar.gz

Next from the ``Download`` Folder we execute  a script that will configure and build vtk in the off-screen mode

Here is the full script:

.. code-block:: bash

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

Compiling CC3D on BigRed2
=========================

This part is relatively simple. All you need to do is clone git repository with CC3D sources and run compilation script
Let's start:

.. code-block:: console

    mkdir ~/CC3D_GIT
    cd ~/CC3D_GIT

    git clone https://github.com/CompuCell3D/CompuCell3D.git .

    git checkout 3.7.9

Now that you have CC3D source we run installation script. Here is the full content of the script:

.. code-block:: bash

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

After this step your cc3d installation should be ready.

If you are bundling cc3d i.e. want to include full Python27 distributiuon (which is an exact copy of your cc3d_377 env
we created earlier)

you also need to change path to python exec env variable in CC3D run scripts

i.e. replace

.. code-block:: console

    export PYTHON_EXEC=/N/u/mswat/BigRed2/.conda_envs/cc3d_377/bin/python

with

.. code-block:: console

    export PYTHON_EXEC=${PREFIX_CC3D}/Python27/bin/python


in all .sh scripts in CC3D install folder


There is one thing you need to fix manually for now:

Go to player5/GraphicsOffscreen/GenericDrawer.py and comment out the following lines:

.. code-block:: python


    #if drawing_params.screenshot_data.lattice_axes_on:
    #    try:
    #        self.draw_axes(drawing_params=drawing_params)
    #    except NotImplementedError:
    #        pass

For some reason rendering of axes doe s not work on BigRed2 with VTK-6.3.0

Installing RoadRunner
=====================


After you install conda environment that includes numpy youu may want to install ``libroadrunner`` normally you would type

.. code-block:: console

    pip install libroadrunner

and ``libroadrunner`` will get installed.

if you run python and there type

.. code-block:: python

    import roadrunner

you should see that import succeeded.

Sometimes you will get an error compaining about wrong version of numpy :

"""module compiled against API version 0xc but this version of numpy is 0xb"

in this situation you may need to install a different version of libroadrunner

to check available versions of libroadrunner you could use a pip hack:

.. code-block:: console

    pip install libroadrunner==

you will get pip error message that will include all available versions of libroadrunner.

then you would uninstall existing libroadrunner (the one that has numpy version conflict):

.. code-block:: console

    pip uninstall libroadrunner

and install new version

.. code-block:: console

    pip install libroadrunner==1.4.24

This typically should fix your problems

