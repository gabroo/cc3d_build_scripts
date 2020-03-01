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


