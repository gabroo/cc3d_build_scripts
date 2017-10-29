import os
from os.path import *

# this is the path to the NSIS instaler executable
NSIS_EXE_PATH = 'C:\Program Files (x86)\NSIS\makensis.exe '
# CMAKE_PATH=os.path.abspath('C:/Program Files (x86)/CMake-3.3.2/bin/cmake.exe')
CMAKE_PATH = abspath('C:/Program Files (x86)/CMake/bin/cmake.exe')
CMAKE_GENERATOR_NAME = 'NMake Makefiles'
WIN_INSTALLER_CREATOR = 'win_cc3d_installer_creator.py'

PYQT_VERSION = 5
WIN_DEPENDENCIES_ROOT = abspath('d:/prerequisites_2017/64bit')
PYTHON_DIR = abspath(join(WIN_DEPENDENCIES_ROOT, 'Python27'))
PYTHON_EXECUTABLE = abspath(join(PYTHON_DIR, 'python.exe'))
PYTHON_INCLUDE_DIR = abspath(join(PYTHON_DIR, 'include'))
PYTHON_LIBRARY = abspath(join(PYTHON_DIR, 'libs/python27.lib'))
# VTK_DIR = os.path.abspath('D:/CC3D_LIBS/VTK-6.3.0_install/lib/cmake/vtk-6.3')
# VTK_DIR = os.path.abspath('D:/zipy/VTK-6.3.0_install/lib/cmake/vtk-6.3')
VTK_DIR = abspath(join(PYTHON_DIR, 'Library/lib/cmake/vtk-6.3'))

# OPENCL_LIBRARIES = os.path.abspath('C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v5.5/lib/x64/OpenCL.lib')
OPENCL_LIBRARIES = os.path.abspath('c:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v8.0/lib/x64/OpenCL.lib')

