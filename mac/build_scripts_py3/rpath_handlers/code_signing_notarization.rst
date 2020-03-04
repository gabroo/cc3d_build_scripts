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