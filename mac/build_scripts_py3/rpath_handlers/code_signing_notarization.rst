Preparing conda installation
============================
We compile CC3D on OSX 10.9 and do notarization/signing on OSX 10.14

Let us first build conda environment that we will use to compile signed and notarized version of
CC3D. To do so we run the following

.. code-block:: console

    conda create -n cc3d_2021 python=3.7

This will create conda environment called ``cc3d_2021`` and ``python version 3.7`` will be the only version
installed. It is important to ensure that ``conda-forge`` is the chanel you are getting code from
because we will be installing packages that are unavailable in the default conda channel

Let us activate the environment:

.. code-block:: console

    conda activate cc3d_2021

After we set up basic ``cc3d_2021`` environment and activated it we need to add more packages
that are necessary for CC3D:

.. code-block:: console

    conda install -c conda-forge numpy scipy pandas jinja2 webcolors vtk=8.2 pyqt=5.6.0 pyqtgraph deprecated qscintilla2 jinja2 chardet cmake swig=3 python.app


Now, to fix possible issues with missing development libraries for tbb (dependency of VTK) we also
install ``tbb_full_dev`` package from ``compucell3d`` channel. This package contains
dependencies (library + header files) for tbb library

.. code-block:: console

     conda install -c compucell3d tbb_full_dev

Next we install libroadrunner by running:

.. code-block:: console

    pip install libroadrunner


The basic installation is there. Now, let us copy ``~/miniconda3/envs/cc3d_2021`` to ``~/prerequisites/4.1.2/python37``

.. code-block:: console

    mkdir -p ~/prerequisites/4.1.2/python37 & cp -R -p ~/miniconda3/envs/cc3d_2021/* ~/prerequisites/4.1.2/python37

Creating compucell3d.app and twedit++.app
=========================================

For CC3D to work properly on OSX we need to run it using ``python.app`` package. This will ensure
that our GUIs behave correctly. All we need to do in this section is to copy
``~/prerequisites/4.1.2/python37/python.app`` to ``~/prerequisites/4.1.2/python37/compucell3d.app`` and to ``~/prerequisites/4.1.2/python37/twedit++.app``. Next, in each of those app bundles (i.e. in ``compucell3d.app`` and ``twedit++.app``) we modify ``Contents/Info.plist`` file and add
replace ``<string>python</string>`` with ``<string>CompuCell3D</string>`` and
``<string>Twedit++</string>`` respectively


Fixing ctypes __init__.py after signing
========================================

In this section we will comment out unneeded one line in ctypes/__init__.py file. It turns out
that after signing python package numpy will not import properly. The line to comment out looks
as follows: ``CFUNCTYPE(c_int)(lambda: None)``

Here is more explanation

https://www.bountysource.com/issues/63856438-update-macos-to-mojave-then-vim-get-error-with-powerline
After code-signign importing numpy may result in MemoryError to fix this we need to
modify ctypes __init__.py

265 def _reset_cache():
266     _pointer_type_cache.clear()
267     _c_functype_cache.clear()
268     if _os.name in ("nt", "ce"):
269         _win_functype_cache.clear()
270     # _SimpleCData.c_wchar_p_from_param
271     POINTER(c_wchar).from_param = c_wchar_p.from_param
272     # _SimpleCData.c_char_p_from_param
273     POINTER(c_char).from_param = c_char_p.from_param
274     _pointer_type_cache[None] = c_void_p
275     # XXX for whatever reasons, creating the first instance of a callback
276     # function is needed for the unittests on Win64 to succeed.  This MAY
277     # be a compiler bug, since the problem occurs only when _ctypes is
278     # compiled with the MS SDK compiler.  Or an uninitialized variable?
279     CFUNCTYPE(c_int)(lambda: None)
As you can see, CFUNCTYPE function at line 279 is added by unittest on Win64 for whatever reasons. For mac user, this line is useless and lead to memory error on macOS. So I comment out line 279, and rerun vim, there is no errors with powerline.


Adding compiler libraries
=========================

CC3D uses gcc 4.8 compiler installed via Homebrew system. Homebrew gcc compilers have proper
OpenMP implementation that default OSX compilers lack. Because of that we also need to distribute
some libraries from the homebrew gcc - in fact there are three libraries - ``libgcc`` ``libstdc++`` and ``libgomp``. In my gcc installation they are located in
``/usr/local/Cellar/gcc48/4.8.2/lib/gcc/x86_64-apple-darwin13.0.2/4.8.2``. The actual names of
libraries that I will add to the prerequisite folder are: ``libgcc_s.1.dylib``,
``libgomp.1.dylib``, ``libstdc++.6.dylib``. I will copy those libraries to
``~/prerequisites/4.1.2/lib/site-packages/cpp``. The reason I pick this directory hierarchy is
because C++ libraries from CC3D will go to ``<CC3D_install_dir>/lib/site-packages/cpp``


Code-signing python distribution
================================

**Important:**

This step has to be performeb on OSX 10.13 or above

Once we prepared our distribution we need to code-sign it. We will use convenience script from
cc3d_build_scripts_repo. The script is located in ``mac/build_scripts_py3/rpath_handlers`` and
is called ``recursive_code_sign``. Since Python distribution contains a lot of files we will
sign only those that need to be signed - binaries and executable. To shorten run time of the script
we will specify subdirectories of ``python37``



In particular this is the list of subdirs where files need to be recursively signed:

<python_dir>/bin
<python_dir>/lib
<python_dir>/libexec
<python_dir>/plugins
<python_dir>/qml
<python_dir>/sbin
<python_dir>/share/cmake-3.16


/Users/m/prerequisites/4.1.2/python37


Building CC3D package
=====================

At this point we can build CC3D package. We will use``/Users/m/CC3D_BUILD_SCRIPTS_GIT/mac/build_scripts_py3/build_script_dmg.py`` script that does not copy python
from prerequisite folder


order

1.fix rparh
2. codesign

CC3D Code Signing and Authorization
===================================

To distribute code on the new OSX you need to sign and notarize binaries. This is a
multiple step process. We will discuss all those steps. We developed convenience scripts that help and automate some of the more mundane tasks related to proper binaries certification

Step 1
-------

In this step we need to make sure that our code can run without specifying
``DYLD_LIBRARY_PATH`` environment variable. In particular we need to make sure there are
no hard-coded paths(except for system libraries) in any shared library we want to
distribute.

**IMPORTANT**. It is best to perform this step first before attempting code signing or
notarization. In our early  tests it happened that if we firss signed code and then
attempted to replace hard-coded path with @rpath specifications we ran into issues




Step 2 - Signing of the code
----------------------------

First make sure you have the proper certificate. The right certificate should read:

**macOS Developer ID XXX**

or if you open Keychain Access application look for certificate that reads
**Developer ID Application: CERTIFICATE_NAME (XXX)**

You may also follow this guide to see if certificate is valid
https://support.apple.com/guide/keychain-access/determine-if-a-certificate-is-valid-kyca2794/mac

From command line if you want to list code signing identities do the following:

.. code-block:: console

    security find-identity -v -p codesigning

see also:
https://stackoverflow.com/questions/7747230/determining-codesigning-identities-from-the-command-line

Here are other useful links

https://ohanaware.com/support/index.php?article=how-to-code-sign-dmg-files.html
https://stackoverflow.com/questions/49748988/how-to-codesign-dmg-and-app-inside-it
https://osxdaily.com/2016/03/14/verify-code-sign-apps-mac-os-x/

Now lets sign directory with cc3d install
We assume that CC3D is installed in ``/Users/m/mini_cc3d_install_1``

.. code-block::

    



Note:
-----

Libraries that are hardcoded are idelly placed in the "deepest library folder"
https://www.bountysource.com/issues/63856438-update-macos-to-mojave-then-vim-get-error-with-powerline
After code-signign importing numpy may result in MemoryError to fix this we need to
modify ctypes __init__.py

265 def _reset_cache():
266     _pointer_type_cache.clear()
267     _c_functype_cache.clear()
268     if _os.name in ("nt", "ce"):
269         _win_functype_cache.clear()
270     # _SimpleCData.c_wchar_p_from_param
271     POINTER(c_wchar).from_param = c_wchar_p.from_param
272     # _SimpleCData.c_char_p_from_param
273     POINTER(c_char).from_param = c_char_p.from_param
274     _pointer_type_cache[None] = c_void_p
275     # XXX for whatever reasons, creating the first instance of a callback
276     # function is needed for the unittests on Win64 to succeed.  This MAY
277     # be a compiler bug, since the problem occurs only when _ctypes is
278     # compiled with the MS SDK compiler.  Or an uninitialized variable?
279     CFUNCTYPE(c_int)(lambda: None)
As you can see, CFUNCTYPE function at line 279 is added by unittest on Win64 for whatever reasons. For mac user, this line is useless and lead to memory error on macOS. So I comment out line 279, and rerun vim, there is no errors with powerline.

also need to sign everything in share/cmake-3.16/

this is what is being signed in python:
<python_dir>/bin
<python_dir>/lib
<python_dir>/libexec
<python_dir>/plugins
<python_dir>/qml
<python_dir>/sbin
<python_dir>/share/cmake-3.16