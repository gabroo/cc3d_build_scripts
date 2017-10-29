# example command:
# c:\miniconda64\python .\win_cc3d_builder_377.py  -p D:/install_projects/3.7.7-64bit -s D:/CC3D_GIT  -i D:/CC3D_FILES_SVN/binaries/3.7.7/windows -v 3.7.7.0


import subprocess
import time
from utils import *

# MAJOR_VERSION = 3
# MINOR_VERSION = 7
# BUILD_VERSION = 7
#
# version_string = '3.7.7'
# win_installer_creator = 'win_cc3d_installer_creator_377.py'


# def printRuntime(_timeInterval):
#     timeInterval = int(_timeInterval)
#     hours = timeInterval / (3600 * 1000)
#     minutesInterval = timeInterval % (3600 * 1000)
#     minutes = minutesInterval / (60 * 1000)
#     secondsInterval = minutesInterval % (60 * 1000)
#     seconds = secondsInterval / (1000)
#     miliseconds = secondsInterval % (1000)
#
#     print "Build RUNTIME ",
#     if hours:
#         print hours, " h : ", minutes, " m : ", seconds, " s : ", miliseconds, " ms"
#     elif minutes:
#         print minutes, " m : ", seconds, " s : ", miliseconds, " ms"
#     elif seconds:
#         print seconds, " s : ", miliseconds, " ms"
#     else:
#         miliseconds, " ms"
#     print "EQUIVALENT OF      %0.3f seconds" % (_timeInterval / 1000)
#
#
# def shellquote(s):
#     return "'" + s.replace("'", "'\\''") + "'"


t1 = time.time()

# # this is the path to the NSIS instaler executable
# NSIS_EXE_PATH = 'C:\Program Files (x86)\NSIS\makensis.exe '
# # CMAKE_PATH=os.path.abspath('C:/Program Files (x86)/CMake-3.3.2/bin/cmake.exe')
# CMAKE_PATH = os.path.abspath('C:/Program Files (x86)/CMake/bin/cmake.exe')
#
# CMAKE_GENERATOR_NAME = 'NMake Makefiles'

# version has to have format 3.7.6.0 - four numbers otherwise NSIS crashes, strange...

# -------------- parsing command line
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-p", "--prefix", dest="prefix", action="store", type=str, help="CC3D installation directory", required=True)
parser.add_argument("-s", "--source-root", dest="source_root", action="store", type=str, default='D:/CC3D_GIT',
                  help="CC3D git repository")

parser.add_argument('-i', '--installer-dir', dest='installer_dir', action='store', type=str, default='',
                  help='Location of the place where to store installer', required=True)
parser.add_argument("-v", "--version", dest="version", action="store", type=str, help='version of installer', required=True)

parser.add_argument("--32bit", dest="arch_32bit", action="store_true", default=False, help='enables 32-bit build architecture')

parser.add_argument("--gpu", dest="arch_gpu", action="store_true", default=False, help='enables generation of gpu modules')

parser.add_argument("-c", "--cores", dest="cores", action="store", type=int, default=1,
                  help="Number of compilation threads for make")

# parser.add_argument("--cc3d", action="store_true", default=False, dest="cc3d",
#                   help='this option picks CompuCell3D to be compiled. Using it will require all other project files to be set individually')
# parser.add_argument("--bionet", action="store_true", default=False, dest="bionet",
#                   help='this option picks BionetSolver to be compiled. Using it will require all other project files to be set individually')
# parser.add_argument("--celldraw", action="store_true", default=False, dest="celldraw",
#                   help='this option picks BionetSolver to be compiled. Using it will require all other project files to be set individually')
# parser.add_argument("--rr", action="store_true", default=False, dest="rr",
#                   help='this option picks RR to be compiled. Using it will require all other project files to be set individually')
# parser.add_argument('--build-installer',action='store_true', default=False, dest="build_installer",help='this option tells the script to build windows installer')



args = parser.parse_args()
# -------------- end of parsing command line

if args.arch_32bit:
    from configs_32bit import *
else:
    from configs_64bit import *


MAJOR_VERSION, MINOR_VERSION, BUILD_VERSION, INSTALLER_BUILD = version_str_to_tuple(args.version)


version_str = version_tuple_to_str(version_component_sequence=(MAJOR_VERSION, MINOR_VERSION, BUILD_VERSION),
                                      number_of_version_components=3)

installer_version_str = version_tuple_to_str(version_component_sequence=(MAJOR_VERSION, MINOR_VERSION, BUILD_VERSION, INSTALLER_BUILD),
                                      number_of_version_components=3)



CURRENT_DIR = os.getcwd()

BUILD_INSTALLER = False
# version_str = options.version

INSTALLER_DIR = args.installer_dir
if INSTALLER_DIR != '':
    INSTALLER_DIR = os.path.abspath(INSTALLER_DIR)
    BUILD_INSTALLER = True

# BUILD_INSTALLER=options.build_installer
# INSTALLER_VERSION = args.version

# HOME_DIR = expanduser('~')

SOURCE_ROOT = os.path.abspath(args.source_root)
INSTALL_PREFIX = os.path.abspath(args.prefix)
BUILD_ROOT = os.path.abspath(INSTALL_PREFIX + '_build')
DEPENDENCIES_ROOT = os.path.abspath(INSTALL_PREFIX + '_depend')

# these are hard-coded for now
# WIN_DEPENDENCIES_ROOT=os.path.abspath('D:/CC3D_FILES_SVN/dependencies/windows/VS2010/dependencies_qt_4.8.5_pyqt_4.10.3_vtk_5.10.1_python27')
# PYQT_VERSION = 5
# WIN_DEPENDENCIES_ROOT = abspath('d:/prerequisites_2017/64bit')
# PYTHON_DIR = abspath(join(WIN_DEPENDENCIES_ROOT, 'Python27'))
# PYTHON_EXECUTABLE = abspath(join(PYTHON_DIR, 'python.exe'))
# PYTHON_INCLUDE_DIR = abspath(join(PYTHON_DIR, 'include'))
# PYTHON_LIBRARY = abspath(join(PYTHON_DIR, 'libs/python27.lib'))
# # VTK_DIR = os.path.abspath('D:/CC3D_LIBS/VTK-6.3.0_install/lib/cmake/vtk-6.3')
# # VTK_DIR = os.path.abspath('D:/zipy/VTK-6.3.0_install/lib/cmake/vtk-6.3')
# VTK_DIR = abspath(join(PYTHON_DIR, 'Library/lib/cmake/vtk-6.3'))
#
# # OPENCL_LIBRARIES = os.path.abspath('C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v5.5/lib/x64/OpenCL.lib')
# OPENCL_LIBRARIES = os.path.abspath('c:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v8.0/lib/x64/OpenCL.lib')

# LIBSBML_INSTALL_DIR=os.path.abspath('D:/CC3D_FILES_SVN/dependencies/windows/VS2010/BionetSolver/sbml-xml2') # used by bionet solver on windows
# SUNDIALS_INSTALL_DIR=os.path.abspath('D:/CC3D_FILES_SVN/dependencies/windows/VS2010/BionetSolver/sundials') # used by bionet solver on windows
# RR_BINARIES_DIR=os.path.abspath('D:/CC3D_FILES_SVN/dependencies/windows/VS2010/roadrunner_1.0.1/')
# WIN_INSTALLER_CREATOR = win_installer_creator

BUILD_CC3D = False
# BUILD_BIONET = False
# # BUILD_BIONET_DEPEND=False
# BUILD_CELLDRAW = False
# BUILD_RR = False
# BUILD_RR_DEPEND = False
# BUILD_ALL = True
MAKE_MULTICORE = 1

# if options.cc3d:
#     BUILD_ALL = False
#     BUILD_CC3D = True
#
# if options.bionet:
#     BUILD_ALL = False
#     BUILD_BIONET = True
#
# if options.celldraw:
#     BUILD_ALL = False
#     BUILD_CELLDRAW = True
#
# if options.rr:
#     BUILD_ALL = False
#     BUILD_RR = True
#
# if BUILD_ALL:
#     BUILD_CC3D = True
#     # BUILD_BIONET=True
#     # BUILD_BIONET_DEPEND=True
#     BUILD_CELLDRAW = True
#     # BUILD_RR=True
#     # # # BUILD_RR_DEPEND=True

if not os.path.isdir(BUILD_ROOT):
    os.makedirs(BUILD_ROOT)

if not os.path.isdir(DEPENDENCIES_ROOT):
    os.makedirs(DEPENDENCIES_ROOT)

# if BUILD_CC3D:
############ building CompuCell3D


CC3D_BUILD_PATH = os.path.abspath(os.path.join(BUILD_ROOT, 'CompuCell3D'))
CC3D_SOURCE_PATH = os.path.abspath(os.path.join(SOURCE_ROOT, 'CompuCell3D'))
if not os.path.isdir(CC3D_BUILD_PATH):
    os.makedirs(CC3D_BUILD_PATH)
os.chdir(CC3D_BUILD_PATH)
print CMAKE_PATH
# subprocess.call([CMAKE_PATH])

cmake_args = [CMAKE_PATH, '-G', CMAKE_GENERATOR_NAME, '-DCMAKE_BUILD_TYPE:STRING=RelWithDebInfo',
                 '-DCMAKE_INSTALL_PREFIX:PATH=' + INSTALL_PREFIX,
                 '-DCOMPUCELL3D_A_MAJOR_VERSION:STRING=' + str(MAJOR_VERSION),
                 '-DCOMPUCELL3D_B_MINOR_VERSION:STRING=' + str(MINOR_VERSION),
                 '-DCOMPUCELL3D_C_BUILD_VERSION:STRING=' + str(BUILD_VERSION),
                 '-DPYTHON_EXECUTABLE=' + PYTHON_EXECUTABLE, '-DPYTHON_INCLUDE_DIR=' + PYTHON_INCLUDE_DIR,
                 '-DPYTHON_LIBRARY=' + PYTHON_LIBRARY,
                 '-DVTK_DIR=' + VTK_DIR,
                 '-DPYQT_VERSION:STRING=' + str(PYQT_VERSION),
                 '-DWINDOWS_DEPENDENCIES:PATH=' + WIN_DEPENDENCIES_ROOT, CC3D_SOURCE_PATH]



if args.arch_gpu:
    cmake_args += ['-DNO_OPENCL:BOOLEAN=OFF',] # enable open_cl - note the option is NO_OPENCL
else:
    cmake_args += ['-DNO_OPENCL:BOOLEAN=ON', ] # disable open_cl note the option is NO_OPENCL

subprocess.call(cmake_args)

# subprocess.call(['nmake'])
subprocess.call(['nmake', 'install'])
############ End of building CompuCell3D

# if BUILD_CELLDRAW:
#
#     ############# BUILDING  CELLDRAW
#     CELLDRAW_BUILD_PATH = os.path.abspath(os.path.join(BUILD_ROOT, 'CellDraw'))
#     CELLDRAW_SOURCE_PATH = os.path.abspath(os.path.join(SOURCE_ROOT, 'CellDraw/1.5.1'))
#
#     if not os.path.isdir(CELLDRAW_BUILD_PATH):
#         os.makedirs(CELLDRAW_BUILD_PATH)
#     os.chdir(CELLDRAW_BUILD_PATH)
#
#     subprocess.call([CMAKE_PATH, '-G', CMAKE_GENERATOR_NAME, '-DCMAKE_BUILD_TYPE:STRING=Release',
#                      '-DCMAKE_INSTALL_PREFIX:PATH=' + INSTALL_PREFIX, CELLDRAW_SOURCE_PATH])
#     subprocess.call(['nmake', 'install'])
#
#     ############# END OF  CELLDRAW
#


if BUILD_INSTALLER:
    # revision number
    # from datetime import date
    #
    # today = date.today()
    # revisionNumber = str(today.year) + str(today.month).zfill(2) + str(today.day).zfill(2)
    # version_str = options.version

    revision_number = timestamp_revision_number()
    INSTALLER_NAME = os.path.abspath(
        os.path.join(INSTALLER_DIR, 'CompuCell3D-64bit-setup-' + version_str + 'v' + revision_number + '.exe'))

    os.chdir(CURRENT_DIR)
    subprocess.call(
        ['python', WIN_INSTALLER_CREATOR, '-d', INSTALL_PREFIX, '-v', installer_version_str, '-i', INSTALLER_NAME])

t2 = time.time()

printRuntime((t2 - t1) * 1000.0)
