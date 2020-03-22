order

1.fix rparh
2. codesign


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


Fixing ctypes __init__.py after signing (obsolete when using entitlement file to sign python distribution)
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


Additionally we will need to to the same fix in 

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

**IMPORTANT** make sure that libraries you copy have write permissions set otherwise you will not be
able to modify rpath in them

libroadrunner
==============

Currently on OSX 10.9 libroadrunner is on version 1.5.6, this version does not work
on OSX 10.14+ therefore, we need to prepare separate binaries for OSX 10.14+. This is not
ideal but once we get updated libroadrunner binaries this limitation will be resolved

gcc compilers on OSX 10.14
==========================

Getting right compiler on OSX that supports OpenCL can be challenging. After few attempts
we determined that gcc@6 from homebrew performs best. All other compilers had issues during
compilation or during runtime. This is not surprising and we sa this behavior in the past

OpenCL solvers on OSX 10.14+
============================

OpenCL solvers on OSX 10.14 + do not work. It is likely that this is connected with
Apple decision to stop support openCL starting with OSX 10.14. for the time being we
recommend that if you need OpenCL solvers on OSX you use OSX 10.13 or lower.

You can always run this operating system from external SSD so that you do not need to
uninstall your latest OSX that you are using. This is not ideal but it is a solution while
we research fixes to this problem


Code-signing python distribution
================================
**Important:** :This step has to be performed on OSX 10.13 or above

Once we prepared our distribution we need to code-sign it. We will use convenience script from
cc3d_build_scripts_repo. The script is located in ``mac/build_scripts_py3/rpath_handlers`` and
is called ``recursive_code_sign``. Since Python distribution contains a lot of files we will
sign only those that need to be signed - binaries and executable. To shorten run time of the script
we will specify subdirectories of ``python37``

In particular this is the list of subdirs where files need to be recursively signed:

<python_dir>/python.app
<python_dir>/compucell3d.app
<python_dir>/twedit++.app
<python_dir>/bin
<python_dir>/lib
<python_dir>/libexec
<python_dir>/plugins
<python_dir>/qml
<python_dir>/sbin
<python_dir>/share/cmake-3.16


Signing python distribution for CC3D requires extra care. Since CC3D relies on ``roadrunner`` package
we need to make sure that ``roadrunner`` works properly within signed Python distribution.
In particular, since ``roadrunner`` generates JIT-code when loading SBML model modern OSX
will not allow this to run unless we add extra entitlements during Python distribution code-signing.
To do that we prepare and XML file called ``entitlements.plist`` and its content looks as follows:

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
      <dict>
        <key>com.apple.security.cs.allow-jit</key>
        <true/>
        <key>com.apple.security.cs.allow-unsigned-executable-memory</key>
        <true/>
        <key>com.apple.security.cs.disable-executable-page-protection</key>
        <true/>
        <key>com.apple.security.cs.disable-library-validation</key>
        <true/>
        <key>com.apple.security.cs.allow-dyld-environment-variables</key>
        <true/>
      </dict>
    </plist>

We will pass this file to the code-signing function so that the invocation of the ``codesign`` tools
looks as follows:

.. code-block:: console

    codesign  -v -s "<certificate_label>" -f --entitlement <entitlement_file> --keychain <keychain_path> <binary_file_to_be_signed>

Obviously we do not want to repeat this call manually so instead we create a convenience script that we
run only once - when we prepare signed distribution of python to be bundled with the rest of CC3D. See
``mac/build_scripts_py3/rpath_handlers/python_recursive_sign.py``

For convenience we present the entire content of this script:

.. code-block:: python

    from recursive_code_sign import codesign_directory_entitlement
    from os.path import *

    python_install_dir = '/Users/m/prerequisites/4.1.2_10.14/python37_signed_entitlements'
    entitlement_file = '/Users/m/CC3D_BUILD_SCRIPTS_GIT/mac/build_scripts_py3/rpath_handlers/entitlements.plist'

    sub_dirs_to_sign = ['bin', 'lib', 'libexec', 'plugins', 'qml', 'sbin', 'share/cmake-3.16',
                        'compucell3d.app', 'twedit++.app', 'python.app', 'Contents']
    certificate_label = "Developer ID Application: Indiana University (5J69S77A7G)"
    keychain_path = "/Users/m/Library/Keychains/login.keychain-db"

    for sub_dir in sub_dirs_to_sign:
        directory = join(python_install_dir, sub_dir)
        codesign_directory_entitlement(
            directory=directory, certificate_label=certificate_label, keychain_path=keychain_path,
            entitlement_file=entitlement_file)


To check entitlements of a binary file follow this example:

.. code-block:: console

    codesign -d --entitlements :- <full_path_to_the_file>

The important thing is that you run this step only when you change python environment which is not that
often. Think of it as a one-time setup task. You do it and then use signed package.

It is worth mentioning that when you build CC3D on OSX 10.9 you use unsigned version but when you
build.dmg that will contain python and is to be notarized you used signed version but you do those steps
on OSX 10.13 or above

In the future we will develop a solution that runs fully on one platform

Building CC3D package
=====================

At this point we can build CC3D package. We will use``/Users/m/CC3D_BUILD_SCRIPTS_GIT/mac/build_scripts_py3/build_script_dmg.py`` script that does not copy python
from prerequisite folder


Fixing hard-coded paths in CC3D libraries
=========================================

When CC3D gets compiled those 3 gcc compiler libraries appear as hard-coded dependencies of CC3D libraries.
We can use script ``rpath_printout`` to ge a list of all hardcoded libraries in the CC3D package. When we run it as

.. code-block:: console

    python rpath_printout.py --directory=/Users/m/install_projects/CC3D_4.1.2
    --extensions
    .dylib
    .so


we will see which libraries have hardcoded paths. We are only interested in "non-system" libraries and in our case
those are:

/usr/local/Cellar/gcc48/4.8.2/lib/gcc/x86_64-apple-darwin13.0.2/4.8.2/libgcc_s.1.dylib
/usr/local/lib/gcc/x86_64-apple-darwin13.0.2/4.8.2/libstdc++.6.dylib
/usr/local/lib/gcc/x86_64-apple-darwin13.0.2/4.8.2/libgomp.1.dylib

We keep a note of them and we will use them in the next script that wil fix hard coded paths for every CC3D liubrary

Running rpath_fixer
--------------------

``rpath_fixer`` is a script that replaces hardcoded library with @rpath counterpart. @rpath stands for runtime search
path. The process of replacing it has two components. First we add a new search path to the dependent library using
``install_name_tool -add_rpath @loader_path/... ...`` command and in step 2 we use ``install_name_tool -change ...``
command to replace hardcoded path with @rpath/path_to_dependent_library

The script does those steps automatically. In out case since we know which 3 libraries are hardcoded we run the script
as follows:

.. code-block:: console


    python rpath_fixer.py
    --directory=/Users/m/install_projects/CC3D_4.1.2
    --extensions
    .dylib
    .so
    --target-location-of-hardcoded-libs=/Users/m/install_projects/CC3D_4.1.2/lib/site-packages/cc3d/cpp/lib
    --hardcoded-paths-list
    /usr/local/Cellar/gcc48/4.8.2/lib/gcc/x86_64-apple-darwin13.0.2/4.8.2/libgcc_s.1.dylib
    /usr/local/lib/gcc/x86_64-apple-darwin13.0.2/4.8.2/libstdc++.6.dylib
    /usr/local/lib/gcc/x86_64-apple-darwin13.0.2/4.8.2/libgomp.1.dylib

where the argument ``--target-location-of-hardcoded-libs`` points to location of the folder in the CC3D install
directory where we will copy the 3 gcc compiler libraries

Although we show this step as standalone step, we integrated this into CC3D build script



Code Signing
=============

Once we signed python distribution and compiled cc3d we run a script that finalizes installation. What it does is
first sign CC3D code, second copy signed pyt distribution:

you run this code as follows:

.. code-block:: console

    python finalize_cc3d_install.py
    --cc3d-install-dir=/Volumes/mavericksosx/Users/m/install_projects/CC3D_4.1.2
    --certificate-label="Developer ID Application: XXX"
    --python-source-signed-dir=/Users/m/prerequisites/4.1.2_10.14/python37_signed_entitlements
    --keychain-path=/Users/m/Library/Keychains/login.keychain-db

Building dmg
============

we use DMG canvas to build dmg and to do notarization. This si paid software but wort 20$ . Make sure to enable
dmg signing and notarization



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

Useful Links
==============

https://github.com/electron/electron/blob/master/docs/tutorial/mac-app-store-submission-guide.md
https://developer.apple.com/videos/play/wwdc2018/702/
https://stackoverflow.com/questions/52911791/hardened-runtime-for-java-and-mojave
https://apple.stackexchange.com/questions/52675/how-do-i-find-out-what-entitlements-an-app-has
https://developer.apple.com/documentation/bundleresources/entitlements/com_apple_security_cs_allow-jit
https://lapcatsoftware.com/articles/hardened-runtime-sandboxing.html
