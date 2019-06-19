Preparing Windows Compilation
=============================

The preparation of windows dependencies can be as simple as downloading a zipped directory from
our download site - https://sourceforge.net/projects/cc3d/files/compile_dependencies/

However, if you are interested in exact steps that are required to prepare those dependencies we present them in
details below

Preparing dependencies
----------------------

Most of windows dependencies can be easily installed using conda
the list of installed packages is stored in ``conda_2020.txt``.

To build this list of exact packages in my conda repository I used the following command

.. code-block:: console

    conda list --explicit > conda_2020.txt

You may use ``conda_2020.txt`` to restore exact packages we installed using the following command

.. code-block:: console

    conda create --name conda_2020 --file conda_2020.txt

This command is not always guaranteed to succeed because conda dependencies are often removed from servers making
this method of freezing dependencies unreliable.

More information about conda can be found on

https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html

However if you install the following packages in your newly created conda environment you should be fine

.. code-block:: console

    conda install -c conda-forge vtk=8.1.0 scipy numpy pandas jinja2 pyqt qscintilla2 webcolors pyqtgraph deprecated pywin32 chardet

The vkt library you install via conda is also used as a dependency for CC3D c++ modules. However, this conda
vtk compilation depends on 3rd party library tbb (Intel's thread building blocks library). Unfortunately this
library is not installed along with vtk so we need to do some minor patching as described below

To install dependencies

Adding TBB to conda environment
-------------------------------

TBB is s C library so all we need to do is to grab binaries for windows from

https://github.com/intel/tbb/blob/master/download.md

For our purposes we used this direct link to grab pre-build windows tbb libraries

https://www.threadingbuildingblocks.org/sites/default/files/software_releases/windows/tbb43_20150611oss_win.zip

Assuming we are building 64-bit application we copy
**IMPORTANT** for 32-bit conda tbb seems to be included so below instrutions apply to 64-bit only conda

``include/tbb`` directory of the tbb binaries into ``c:/Miniconda3/envs/cc3d_2020/Library/include/vtk-8.1`` .


In your case the exact location of conda environment you are creating mught be different . The important part is to go
from the root of the environment - in my case ``c:/Miniconda3/envs/cc3d_2020`` to ``Library/include/vtk-8.1``.

Next we copy  tbb libraries

We grab all files (*.lib extensions) from ``lib/intel64/vc12`` and place them in
``c:/Miniconda3/envs/cc3d_2020/Library/lib``

The procedure for patching 32 bit conda is similar except we would copy all files (*.lib extensions)
from ``lib/ia32/vc12`` and place them inside ``Library/lib`` subfolder of your respective conda root

**Important** We also need to patch ``<python_root>/Python36/Library/lib/cmake/vtk-8.1/VTKTargets.cmake``

replace line

.. code-block:: python

    INTERFACE_LINK_LIBRARIES "\$<\$<NOT:\$<CONFIG:DEBUG>>:C:/Miniconda3/envs/cc3d_2020/Library/lib/tbb.lib>;\$<\$<CONFIG:DEBUG>:C:/Miniconda3/envs/cc3d_2020/Library/lib/tbb.lib>"

with

.. code-block:: python

    INTERFACE_LINK_LIBRARIES "${_IMPORT_PREFIX}/lib/tbb.lib"

This fix is necessary because during installation of vtk on your machine the installing script hard-codes path to
tbb library which is bad (conda issue)

So here we are replacing hardcoded path with a simple statement based on anchor directory cmake variable ${_IMPORT_PREFIX}

This os much better and is guaranteed to work on any machine

Adding libroadrunner
--------------------

After you activate your conda environment you also need to install libroadrunner
The best way is to use ``pip`` command by typing

.. code-block:: console

    pip install libroadrunner

If for some reason (usually incompatibility with your installed numpy version) importing roadrunner fails

you may try different versions of roadrunner. To get a list of available versions available via pip, type:

.. code-block:: console

    pip install libroadrunner==

This  is a bit of a hack but you will get list of libroadrunner versions in the following form

`` Could not find a version that satisfies the requirement libroadrunner== (from versions: 1.4.18, 1.4.23, 1.4.24, 1.5.1, 1.5.2, 1.5.3)
No matching distribution found for libroadrunner==``

Now you can try any particular version by typing for example

.. code-block:: console

    pip install libroadrunner==1.5.1

Updating qt.conf
----------------
In order for qt installation to functionproperly on any system where we distrivuter Python36 we need to
update ``<conda_env>/qt.conf`` as follows

.. code-block:: console

    [Paths]
    Prefix = ./Library
    Binaries = ./Library/bin
    Libraries = ./Library/lib
    Headers = ./Library/include/qt


and ``<conda_env>/Library/bin/qt.conf`` :

.. code-block:: console

    [Paths]
    Prefix = ../
    Binaries = ../bin
    Libraries = ../lib
    Headers = ../include/qt

Updating plugin/platforms - 32bit only
--------------------------------------

For 32bit prerequisites we also need to make sure that ``<conda_env>/Library/plugins/platforms/qwindows.dll``
ends up in  ``<cc3d_install_folder>/bin/platrofms``
so the best way is tro create prerequisites folder ``<prerequisites_folder>/bin/platrofms`` and copy there
the ``qwindows.dll``

Copy icons for NSIS
-------------------

Copy all icons from ``nsis_icons`` to ``c:/Program Files (x86)/NSIS/Contrib/Graphics/Icons/``


Patching pyqtgraph - no longer necessary
----------------------------------------

**Note:** this procedure is no longer necessary . We are including it as a reference of what was required in previous
versions of CC3D and just in case anybody encounters pyqtgraph import issues

In previous versions we had to modify  <conda_env_root>\Lib\site-packages\pyqtgraph\widgets\GraphicsView.py
by replacing

.. code-block:: python

        from .. import _connectCleanup
        _connectCleanup()

with

.. code-block:: python

        from pyqtgraph import _connectCleanup
        _connectCleanup()

        # from .. import _connectCleanup
        # _connectCleanup()

We are not doing it anymore

