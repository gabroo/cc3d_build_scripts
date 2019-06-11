"""
This script builds CC3D on Windows. The arguments are :

--prefix - CC3D installation directory
--source-root - CC3D git repository
--installer_dir - Folder where the installer will be stored
--version - version string - four components is preferred e.g. 3.7.6.0
--gpu  -  indicates whether to build gpu modules. Lack of this option will skip bulding of the OPEN CL objects
--cores -  number of processors to use during compilation - currently not functional witn VS compilers
--config-file - file name of the json file with the specification of paths to various programs/libraries/files
necessary to compile CC3D


example commands:

IMPORTANT add path to cc3d_build_scripts to PYTHONPATH by running:

@SET PYTHONPATH=d:\CC3D_BUILD_SCRIPTS_GIT

1 . 64bit no open cl modules:

c:\Miniconda3\python win_cc3d_builder.py  -p D:/install_projects/4.0.0-64bit -s D:/CC3D_PY3_GIT  -i D:/CC3D_FILES_SVN/binaries/4.0.0/windows -v 4.0.0.0 --config=config_64bit.json

2. 64bit with open cl modules:

c:\Miniconda3\python .\win_cc3d_builder.py -p D:/install_projects/4.0.0-64bit -s D:/CC3D_PY3_GIT  -i D:/CC3D_FILES_SVN/binaries/4.0.0/windows -v 4.0.0.0 --config=config_64bit.json --gpu

3 . 32bit no open cl modules:

c:\Miniconda3\python win_cc3d_builder.py  -p D:/install_projects/4.0.0-32bit -s D:/CC3D_PY3_GIT  -i D:/CC3D_FILES_SVN/binaries/4.0.0/windows -v 4.0.0.0 --config=config_32bit.json

4. 32bit with open cl modules:

c:\Miniconda3\python win_cc3d_builder.py  -p D:/install_projects/4.0.0-32bit -s D:/CC3D_PY3_GIT  -i D:/CC3D_FILES_SVN/binaries/4.0.0/windows -v 4.0.0.0 --config=config_32bit.json --gpu

"""
import time

import os
import subprocess
from argparse import ArgumentParser
import sys
# print sys.path
# import build_utils

from build_utils_py3.build_utils import *
# from utils import *
from build_utils_py3.configs import ConfigsWindows

t1 = time.time()
# version has to have format 3.7.6.0 - four numbers otherwise NSIS crashes, strange...

# -------------- parsing command line
parser = ArgumentParser()
parser.add_argument("-p", "--prefix", dest="prefix", action="store", type=str, help="CC3D installation directory",
                    required=True)
parser.add_argument("-s", "--source-root", dest="source_root", action="store", type=str, default='D:/CC3D_GIT',
                    help="CC3D git repository")

parser.add_argument('-i', '--installer-dir', dest='installer_dir', action='store', type=str, default='',
                    help='Folder where the installer will be stored', required=True)

parser.add_argument("-v", "--version", dest="version", action="store", type=str, help='version of installer',
                    required=True)

parser.add_argument("--gpu", dest="arch_gpu", action="store_true", default=False,
                    help='enables generation of gpu modules')

parser.add_argument("-c", "--cores", dest="cores", action="store", type=int, default=1,
                    help="Number of compilation threads for make")

parser.add_argument("--config-file", dest="config_file", action="store", type=str, default='', required=True,
                    help="configuration file in json format specifying paths of prigams needed to compile CC3D")

args = parser.parse_args()
# -------------- end of parsing command line
CFG = ConfigsWindows(json_fname=args.config_file)

MAJOR_VERSION, MINOR_VERSION, BUILD_VERSION, INSTALLER_BUILD = version_str_to_tuple(args.version)

version_str = version_tuple_to_str(version_component_sequence=(MAJOR_VERSION, MINOR_VERSION, BUILD_VERSION),
                                   number_of_version_components=3)


installer_version_str = version_tuple_to_str(
    version_component_sequence=(MAJOR_VERSION, MINOR_VERSION, BUILD_VERSION, INSTALLER_BUILD),
    number_of_version_components=4)


CURRENT_DIR = os.getcwd()

BUILD_INSTALLER = False
# version_str = options.version

INSTALLER_DIR = args.installer_dir
if INSTALLER_DIR != '':
    INSTALLER_DIR = os.path.abspath(INSTALLER_DIR)
    BUILD_INSTALLER = True

SOURCE_ROOT = os.path.abspath(args.source_root)
INSTALL_PREFIX = os.path.abspath(args.prefix)
BUILD_ROOT = os.path.abspath(INSTALL_PREFIX + '_build')
DEPENDENCIES_ROOT = os.path.abspath(INSTALL_PREFIX + '_depend')

BUILD_CC3D = False
MAKE_MULTICORE = 1

if not os.path.isdir(BUILD_ROOT):
    os.makedirs(BUILD_ROOT)

if not os.path.isdir(DEPENDENCIES_ROOT):
    os.makedirs(DEPENDENCIES_ROOT)

CC3D_BUILD_PATH = os.path.abspath(os.path.join(BUILD_ROOT, 'CompuCell3D'))
CC3D_SOURCE_PATH = os.path.abspath(os.path.join(SOURCE_ROOT, 'CompuCell3D'))
if not os.path.isdir(CC3D_BUILD_PATH):
    os.makedirs(CC3D_BUILD_PATH)
os.chdir(CC3D_BUILD_PATH)

cmake_args = [CFG.CMAKE_PATH, '-G', CFG.CMAKE_GENERATOR_NAME, '-DCMAKE_BUILD_TYPE:STRING=RelWithDebInfo',
              '-DCMAKE_INSTALL_PREFIX:PATH=' + INSTALL_PREFIX,
              '-DCOMPUCELL3D_A_MAJOR_VERSION:STRING=' + str(MAJOR_VERSION),
              '-DCOMPUCELL3D_B_MINOR_VERSION:STRING=' + str(MINOR_VERSION),
              '-DCOMPUCELL3D_C_BUILD_VERSION:STRING=' + str(BUILD_VERSION),
              '-DPYTHON_EXECUTABLE=' + CFG.PYTHON_EXECUTABLE, '-DPYTHON_INCLUDE_DIR=' + CFG.PYTHON_INCLUDE_DIR,
              '-DPYTHON_LIBRARY=' + CFG.PYTHON_LIBRARY,
              '-DPython_EXECUTABLE=' + CFG.PYTHON_EXECUTABLE,
              '-DPython_INCLUDE_DIRS=' + CFG.PYTHON_INCLUDE_DIR,
              '-DPython_LIBRARIES=' + CFG.PYTHON_LIBRARY,
              '-DPython_LIBRARY_RELEASE=' + CFG.PYTHON_LIBRARY,
              '-DVTK_DIR=' + CFG.VTK_DIR,
              '-DWINDOWS_DEPENDENCIES:PATH=' + CFG.WIN_DEPENDENCIES_ROOT, CC3D_SOURCE_PATH]

if args.arch_gpu:
    cmake_args += ['-DNO_OPENCL:BOOLEAN=OFF', '-DOPENCL_LIBRARIES=' + CFG.OPENCL_LIBRARIES,]  # enable open_cl - note the option is NO_OPENCL
else:
    cmake_args += ['-DNO_OPENCL:BOOLEAN=ON', ]  # disable open_cl note the option is NO_OPENCL

subprocess.call(cmake_args)

subprocess.call(['nmake', 'install'])
############ End of building CompuCell3D

# compiling all python code
import compileall
dirs_to_python_compile = ['lib',
                          # 'Demos'
                          ]

for compile_dir in dirs_to_python_compile:
    dir_full_path = os.path.join(INSTALL_PREFIX, compile_dir)
    compileall.compile_dir(dir_full_path, force=True)


if BUILD_INSTALLER:
    revision_number = timestamp_revision_number()

    gpu_tag = '-'
    if args.arch_gpu:
        gpu_tag = '-gpu-'

    INSTALLER_NAME = os.path.abspath(
        os.path.join(INSTALLER_DIR, 'CompuCell3D-' + CFG.BUILD_ARCH_TAG + gpu_tag +
                     'setup-' + version_str + 'v' + revision_number + '.exe'))

    os.chdir(CURRENT_DIR)
    subprocess.call(
        [CFG.PYTHON_EXECUTABLE,
            # 'python',
         CFG.WIN_INSTALLER_CREATOR, '-d', INSTALL_PREFIX, '-v', installer_version_str, '-i', INSTALLER_NAME,
         '-t', CFG.WIN_INSTALLER_TEMPLATE])

t2 = time.time()

printRuntime((t2 - t1) * 1000.0)
