Bundling libraries
==================

On Red Hat systems you may also need to bundle additional graphics-related libraries:
For example on RH 7.5 we put the following:

libGL.so.1       libXext.so
libGL.so.1.2.0   libXext.so.6
libGLU.so        libSM.so            libXext.so.6.4.0
libGLU.so.1      libSM.so.6          libXt.so
libGLU.so.1.3.1  libSM.so.6.0.1      libXt.so.6
libICE.so        libX11.so           libXt.so.6.0.0
libICE.so.6      libX11.so.6
libGL.so         libICE.so.6.3.0  libX11.so.6.3.0

into <CC3D_install_dir>/lib folder
