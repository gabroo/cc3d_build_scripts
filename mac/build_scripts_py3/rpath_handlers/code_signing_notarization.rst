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

    






