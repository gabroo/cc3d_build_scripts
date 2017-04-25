This document describes basic procedure to prepare distribution of CC3D on OSX Mavericks

We assume that we will be using miniconda python distribution (see https://conda.io/miniconda.html). We will install
several CC3D python dependencies using conda installer while others (e.g. VTK) will be installed separately.
The general procedure is that we will first build CC3D from source (which we are not covering in this writeup) and then
move miniconda's python interpreter to CC3D installation subfolder (python27) for self-contained packaging. It turns out
that moving Python intepretter on OSX causes some problems and we are explaining here how to resolve those. This writeup
is bit verbose but it covers in details various gotchas that might not be so obvious.

First let's do some preliminary work

- install miniconda (go to https://conda.io/miniconda.html) and download install script for Python 2.7 for OSX. In my case I downloaded the followng script::

        Miniconda2-latest-MacOSX-x86_64.sh

go to the directory where you downloaded Miniconda2-latest-MacOSX-x86_64.sh and change the permission to executable by typing::

        chmod +x Miniconda2-latest-MacOSX-x86_64.sh

Run the installer::

        ./Miniconda2-latest-MacOSX-x86_64.sh
	
At the end when it asks you whether you want to add path to miniconda to system path , answer "yes" (if you answer "no" - wchih is also OK) you will need to by typing full path to conda's commands such as "activate" etc... ::

        Do you wish the installer to prepend the Miniconda2 install location
        to PATH in your /Users/m/.bash_profile ? [yes|no]
        [yes] >>> yes


- create conda environment for cc3d::

        conda create -n cc3d_2017 python
After you create the environment you have to activate it by typing::

        source activate cc3d_2017

- install dependencies using the following conda command::

        conda install numpy pyqt

See https://conda.io/docs/using/pkgs.html for full documentation on conda

- compile qscintilla in the cc3d_2017 conda environment
To compile qscintilla we download qscintilla from riverbank.com website (https://www.riverbankcomputing.com/software/qscintilla/download)
unpack it and follow 

5) change rpath in the qscintilla's Qsci.so shared library
 a) when you build and install qscintilla in the cc3d_2017 conda environment the Qsci.so library is places in the
 <PATH_TO_CONDA_CC3D_2017_ENV>/lib/python2.7/site-packages/PyQt5

 when you try running e.g. twedit++ after you move to another machine or simply temporarily rename path to your miniconda dir
 you will most likely get the following error:

Traceback (most recent call last):
  File "/Users/m/new_install_projects/CC3D/Twedit++/twedit_plus_plus_cc3d.py", line 28, in <module>
    from utils.global_imports import *
  File "/Users/m/new_install_projects/CC3D/Twedit++/utils/global_imports.py", line 5, in <module>
    from PyQt5.Qsci import *
ImportError: dlopen(/Users/m/new_install_projects/CC3D/python27/lib/python2.7/site-packages/PyQt5/Qsci.so, 2):
Library not loaded: /Users/m/miniconda/envs/pyqt5vtk/lib/libqscintilla2.12.dylib
  Referenced from: /Users/m/new_install_projects/CC3D/python27/lib/python2.7/site-packages/PyQt5/Qsci.so
  Reason: image not found

  The reason is that Qsci.so hard-codes the location of the one of its dependency : libqscintilla2.12.dylib

  How do we know this? Simply by using
otool -L /Users/m/new_install_projects/CC3D/python27/lib/python2.7/site-packages/PyQt5/Qsci.so

the output we get is this (of course in your case the directories might be somewhat different but the general them holds)

/Users/m/new_install_projects/CC3D/python27/lib/python2.7/site-packages/PyQt5/Qsci.so:
	/Users/m/miniconda/envs/pyqt5vtk/lib/python2.7/site-packages/PyQt5/Qsci.so (compatibility version 0.0.0, current version 0.0.0)
	/Users/m/miniconda/envs/pyqt5vtk/lib/libqscintilla2.12.dylib (compatibility version 12.0.0, current version 12.0.2)
	@rpath/libQt5PrintSupport.5.dylib (compatibility version 5.6.0, current version 5.6.2)
	/System/Library/Frameworks/DiskArbitration.framework/Versions/A/DiskArbitration (compatibility version 1.0.0, current version 1.0.0)
	/System/Library/Frameworks/IOKit.framework/Versions/A/IOKit (compatibility version 1.0.0, current version 275.0.0)
	@rpath/libQt5Widgets.5.dylib (compatibility version 5.6.0, current version 5.6.2)
	@rpath/libQt5MacExtras.5.dylib (compatibility version 5.6.0, current version 5.6.2)
	@rpath/libQt5Gui.5.dylib (compatibility version 5.6.0, current version 5.6.2)
	@rpath/libQt5Core.5.dylib (compatibility version 5.6.0, current version 5.6.2)
	/System/Library/Frameworks/OpenGL.framework/Versions/A/OpenGL (compatibility version 1.0.0, current version 1.0.0)
	/System/Library/Frameworks/AGL.framework/Versions/A/AGL (compatibility version 1.0.0, current version 1.0.0)
	/usr/lib/libc++.1.dylib (compatibility version 1.0.0, current version 120.0.0)
	/usr/lib/libSystem.B.dylib (compatibility version 1.0.0, current version 1213.0.0)

The problem is in the third line of the output:

/Users/m/miniconda/envs/pyqt5vtk/lib/libqscintilla2.12.dylib (compatibility version 12.0.0, current version 12.0.2)

this means that during loading of the library the loader searches for libqscintilla2.12.dylib that it expects to find in
/Users/m/miniconda/envs/pyqt5vtk/lib/. Since we are aiming to distribute packages to other users we cannot expect that they will have
/Users/m/miniconda/envs/pyqt5vtk/lib/ on their machines.

the trick is to set run-path (aka @rpath) instead of hardcoded path. @rpath mechanism is designed to tell loader to look for
 dependent libraries in certain directories specified using relative w.r.t to the main program that we are loading. But
 what is this main program and how do we determine the path w.r.t which we are supposed to specify path to libqscintilla2.12.dylib.

 The program we are running is actually python interpreter that will be located in the cc3d distribution directory.

 if we go the the python folder that contains "python" program (in my case it will be
 /Users/m/new_install_projects/CC3D/python27/bin) we can type

 otool -l python and we will get the following output (showing only relevant part here):

 Load command 16
          cmd LC_RPATH
      cmdsize 40
         path @loader_path/../lib/ (offset 12)

This means that when we specify @rpath we will use as a reference point (for relative paths) the path given by
@loader_path/../lib/. In our case this translates to lib directory located one directory up from the
/Users/m/new_install_projects/CC3D/python27/bin/python program which happens to be

/Users/m/new_install_projects/CC3D/python27/lib .

Therefore all the paths we use in the @rpath specifications will be w.r.t  /Users/m/new_install_projects/CC3D/python27/lib.

The libqscintilla2.12.dylib is located in the /Users/m/new_install_projects/CC3D/python27/lib therefore all we have to do is
to change /Users/m/miniconda/envs/pyqt5vtk/lib/libqscintilla2.12.dylib entry in the Qsci.so to @rpath/libqscintilla2.12.dylib

A rule of thumb is to mentally replace @rpath with the path segment that corresponds to the @loader_path/../lib/ of python program
As we have shown this resolves to /Users/m/new_install_projects/CC3D/python27/lib . Therfore since
full path to libqscintilla2.12.dylib is

/Users/m/new_install_projects/CC3D/python27/lib/libqscintilla2.12.dylib

we replace /Users/m/new_install_projects/CC3D/python27/lib with @rpath and hence @rpath/libqscintilla2.12.dylib

How do we modify hardcoded library paths? Using install_name_tool utility. Simply lets go to the location of
Qsci.so (i.e. /Users/m/new_install_projects/CC3D/python27/lib/python2.7/site-packages/PyQt5) and execute the following command:

install_name_tool -change /Users/m/miniconda/envs/pyqt5vtk/lib/libqscintilla2.12.dylib @rpath/libqscintilla2.12.dylib QSci.so

second argument specifies the path to the dependent library we want to replace 3rd argument specifies new path to
the dependent library -  this time using @rpath and the 4th argument is the name of the library whose entries we want to
alter.

Typically one writes appropriate scripts that modify hardcoded paths in the libraries but at least with this installation of conda
Qsci is the only library requiring such modification therefore we present full procedure along with explanation.

As a side note , if you are interested which libraries are loaded during execution of the program on OSX all you have to do is to set

DYLD_PRINT_LIBRARIES environment variable to 1 either in the terminal or in the bash script that you are running:

export DYLD_PRINT_LIBRARIES=1

6) Dealing with Qt "This application failed to start because it could not find or load the Qt platform plugin "cocoa" "
error

The above mentioned error can occur when we move conda installation  with pyqt installed to another directory - in our case
when we are prepping CC3D installation in /Users/m/new_install_projects/CC3D with python interpreter dir placed in
/Users/m/new_install_projects/CC3D/python27 we obviously are moving entire qt installion that was put in place by
conda installer when we issued

conda install pyqt

command.

The reason for the error is quite simple (not simple to locate though ;) ) The problem lies in the content qt.conf
configuration file of Qt. The full path t this file in our CC3D dir is:

/Users/m/new_install_projects/CC3D/python27/bin/qt.conf

The content is:



