Prerequisites
=============

Install miniconda3 on your OSX.

Setup your compiler - see instructions

Next, create environment

.. code-block:: console

    conda create -n cc3d_test_1

Next, install compile and runtime dependencies:

.. code-block:: console
    conda activate cc3d_test_1


Note, you can either install dependencies as shown below from **compucell3d**
channel (**-c compucell3d**) or you may try switching channel and going with
conda-forge channel. **compucell3d** channel stores dependencies that were
downloaded from **conda-forge** but the nice thing about **compucell3d** channel
is that those are exact dependencies we use to build CC3D binaries and therefore we recommend
running the following command:

.. code-block:: console

    conda install conda install -c compucell3d vtk=8.1 scipy numpy=1.16 pandas jinja2 pyqt qscintilla2 webcolors pyqtgraph deprecated  chardet swig=3

If you want o use conda-forge channel you would run

.. code-block:: console

    conda install conda install -c conda-forge vtk=8.1 scipy numpy=1.16 pandas jinja2 pyqt qscintilla2 webcolors pyqtgraph deprecated  chardet swig=3


To ensure that compilation of vtk dependent modules proceeds without errors you need to install
**tbb_full_dev** patch package from **compucell3d** channel:

.. code-block::

    conda install -c compucell3d tbb_full_dev

If you want to run SBMLSoler you need to install libroadrunner and optionally antimony:

.. code-block::

    pip install libroadrunner

.. code-block::

    pip install antimony

Those are pip packages and we do not provide conda packages for those at the moment but pip
installation seems to be reliable.


Compilation
===========

The best way to configure compilation is to start CMake gui (3.13 or higher) directly from the
terminal. If you activate conda environment prior to starting cmake gui from the terminal
many of the paths will be correctly identified:

.. code-block:: console

    conda activate cc3d_test_1

    /Applications/CMake.app/Contents/bin/cmake-gui


Change **CMAKE_INSTALL_PREFIX** to the location you want to install cc3d_to:

in my case I change it to

/Users/m/cc3d_411

Toggle **Advanced** check box in cmake-gui and in the search box type Python. This will display all
Python related cmake variables. As you can see they point to wrong locations of  library include
and executable files. We fix them to point to paths within out **cc3d_test_1** environment as
follows:

.. code-block:: console:

    Python_EXECUTABLE = /Users/m/miniconda3/envs/cc3d_test_1/bin/python
    PYTHON_EXECUTABLE = /Users/m/miniconda3/envs/cc3d_test_1/bin/python
    PYTHON_INCLUDE_DIR = /Users/m/miniconda3/envs/cc3d_test_1/include/python3.7m
    Python_INCLUDE_DIRS = /Users/m/miniconda3/envs/cc3d_test_1/include/python3.7m
    PYTHON_LIBRARY = /Users/m/miniconda3/envs/cc3d_test_1/lib/libpython3.7m.dylib
    Python_LIBRARIES = /Users/m/miniconda3/envs/cc3d_test_1/lib/libpython3.7m.dylib
    Python_LIBRARIES = /Users/m/miniconda3/envs/cc3d_test_1/lib/libpython3.7m.dylib
    Python_LIBRARY_RELEASE = /Users/m/miniconda3/envs/cc3d_test_1/lib/libpython3.7m.dylib

Check swig installation

Click **Configure** and **Generate**

go to cmake binary output folder (in my case **/Users/m/CC3D_PY3_GIT_build_test**)

.. code-block::

    cd /Users/m/CC3D_PY3_GIT_build_test
    make -j 8
    make install

Now, to ensure that run scripts work properly you need to do one final step - create a link
in the cc3d install directory to python environment we used for the installation:

Here is th command that I used (conda python environment I used to compile cc3d is in
/Users/m/miniconda3/envs/cc3d_test_1 and I am creating a python37 soft-link inside
cc3d installation folder):

.. code-block:: console

    ln -s /Users/m/miniconda3/envs/cc3d_test_1 /Users/m/cc3d_411/python37

