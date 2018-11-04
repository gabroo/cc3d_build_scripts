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



