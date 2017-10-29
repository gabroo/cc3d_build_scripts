"""
This script builds CC3D on OSX. The arguments are :

--prefix - CC3D installation directory
--source-root - CC3D git repository
--installer_dir - Folder where the installer will be stored
--version - version string - four components is preferred e.g. 3.7.6.0
--gpu  -  indicates whether to build gpu modules. Lack of this option will skip bulding of the OPEN CL objects
--cores -  number of processors to use during compilation - currently not functional witn VS compilers
--config-file - file name of the json file with the specification of paths to various programs/libraries/files
necessary to compile CC3D


example commands:

1 . 64bit build:

python osx_cc3d_builder.py -p /Users/m/install_projects/CC3D_3.7.7_new -s /Users/m/CC3D_GIT   -v 3.7.7.0 --config=config_64bit.json

"""
import time
from os.path import *
import os
import shutil
import subprocess
from argparse import ArgumentParser
from distutils.dir_util import copy_tree
import datetime
from build_utils.build_utils import *
from build_utils.configs import ConfigsOSX

t1 = time.time()

# -------------- parsing command line
parser = ArgumentParser()
parser.add_argument("-p", "--prefix", dest="prefix", action="store", type=str, help="CC3D installation directory",
                    required=True)
parser.add_argument("-s", "--source-root", dest="source_root", action="store", type=str, default='D:/CC3D_GIT',
                    help="CC3D git repository")

# parser.add_argument('-i', '--installer-dir', dest='installer_dir', action='store', type=str, default='',
#                     help='Folder where the installer will be stored', required=True)
parser.add_argument("-v", "--version", dest="version", action="store", type=str, help='version of installer',
                    required=True)

# parser.add_argument("--32bit", dest="arch_32bit", action="store_true", default=False, help='enables 32-bit build architecture')

parser.add_argument("--gpu", dest="arch_gpu", action="store_true", default=False,
                    help='enables generation of gpu modules')

parser.add_argument("-c", "--cores", dest="cores", action="store", type=int, default=8,
                    help="Number of compilation threads for make")

parser.add_argument("--config-file", dest="config_file", action="store", type=str, default='', required=True,
                    help="configuration file in json format specifying paths of programs needed to compile CC3D")

args = parser.parse_args()
# -------------- end of parsing command line
CFG = ConfigsOSX(json_fname=args.config_file)

MAJOR_VERSION, MINOR_VERSION, BUILD_VERSION, INSTALLER_BUILD = version_str_to_tuple(args.version)

version_str = version_tuple_to_str(version_component_sequence=(MAJOR_VERSION, MINOR_VERSION, BUILD_VERSION),
                                   number_of_version_components=3)

installer_version_str = version_tuple_to_str(
    version_component_sequence=(MAJOR_VERSION, MINOR_VERSION, BUILD_VERSION, INSTALLER_BUILD),
    number_of_version_components=3)

CURRENT_DIR = os.getcwd()

BUILD_INSTALLER = False
# version_str = options.version

# INSTALLER_DIR = args.installer_dir
# if INSTALLER_DIR != '':
#     INSTALLER_DIR = os.path.abspath(INSTALLER_DIR)
#     BUILD_INSTALLER = True

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

print
# cmake\
#    -G "Unix Makefiles" -DPYTHON_MINOR_VERSION:STRING=${PYTHON_MINOR_VERSION}\
#    -DCMAKE_INSTALL_PREFIX:PATH=$INSTALL_PREFIX\
#    -DCOMPUCELL3D_A_MAJOR_VERSION:STRING=$MAJOR_VERSION\
#    -DCOMPUCELL3D_B_MINOR_VERSION:STRING=$MINOR_VERSION\
#    -DCOMPUCELL3D_C_BUILD_VERSION:STRING=${BUILD_VERSION}\
#    -DCMAKE_OSX_DEPLOYMENT_TARGET:STRING=10.9\
#    -DPYQT_VERSION:STRING=5\
#    -DPYTHON_EXECUTABLE:FILEPATH=${MAC_DEPS}/python27/bin/python2.7\
#    -DPYTHON_INCLUDE_DIR:PATH=${MAC_DEPS}/python27/include/python2.7\
#    -DPYTHON_LIBRARY:FILEPATH=${MAC_DEPS}/python27/lib/libpython2.7.dylib\
#    -DEIGEN3_INCLUDE_DIR=${SOURCE_ROOT}/CompuCell3D/core/Eigen\
#    -DCMAKE_C_COMPILER:FILEPATH=${GCC_DIR}/bin/gcc\
#    -DCMAKE_CXX_COMPILER:FILEPATH=${GCC_DIR}/bin/g++\
#    PATH=$INSTALL_PREFIX\
#    -DVTK_DIR:PATH=${VTK_BIN_AND_BUILD_DIR}/lib/cmake/vtk-6.3\
#    -DCMAKE_CXX_FLAGS="-mmacosx-version-min=10.6 -O3 -g -fpermissive -m64"\
#    -DCMAKE_C_FLAGS="-mmacosx-version-min=10.6 -O3 -g -fpermissive -m64"\
#    $SOURCE_ROOT/CompuCell3D


cmake_args = [CFG.CMAKE_PATH, '-G', CFG.CMAKE_GENERATOR_NAME, '-DCMAKE_BUILD_TYPE:STRING=RelWithDebInfo',
              '-DCMAKE_INSTALL_PREFIX:PATH=' + INSTALL_PREFIX,
              '-DPYTHON_MINOR_VERSION:STRING=' + CFG.PYTHON_MINOR_VERSION,
              '-DCMAKE_OSX_DEPLOYMENT_TARGET:STRING=' + CFG.CMAKE_OSX_DEPLOYMENT_TARGET,
              '-DCOMPUCELL3D_A_MAJOR_VERSION:STRING=' + str(MAJOR_VERSION),
              '-DCOMPUCELL3D_B_MINOR_VERSION:STRING=' + str(MINOR_VERSION),
              '-DCOMPUCELL3D_C_BUILD_VERSION:STRING=' + str(BUILD_VERSION),
              '-DPYQT_VERSION:STRING=' + str(CFG.PYQT_VERSION),
              '-DPYTHON_EXECUTABLE:FILEPATH=' + CFG.PYTHON_EXECUTABLE,
              '-DPYTHON_INCLUDE_DIR:PATH=' + CFG.PYTHON_INCLUDE_DIR,
              '-DPYTHON_LIBRARY:FILEPATH=' + CFG.PYTHON_LIBRARY,
              '-DEIGEN3_INCLUDE_DIR:PATH=' + join(SOURCE_ROOT, 'CompuCell3D/core/Eigen'),
              '-DCMAKE_C_COMPILER:FILEPATH=' + CFG.CMAKE_C_COMPILER,
              '-DCMAKE_CXX_COMPILER:FILEPATH=' + CFG.CMAKE_CXX_COMPILER,
              '-DVTK_DIR:PATH=' + CFG.VTK_DIR,
              '-DPYQT_VERSION:STRING=' + str(CFG.PYQT_VERSION),
              'PATH=' + INSTALL_PREFIX,
              CC3D_SOURCE_PATH
              ]

subprocess.call(cmake_args)

subprocess.call(['make', '-j ' + str(args.cores)])
subprocess.call(['make', 'install'])

# copying RR to CC3D install dir:
shutil.copytree(CFG.RR_INSTALL_PATH, join(INSTALL_PREFIX, 'lib/python/roadrunner'))

# packaging CC3D
# cp -a ${MAC_DEPS}/* ${INSTALL_PREFIX}
# -a option does not replace symlinks with files
# subprocess.call(['cp', '-a', CFG.PREREQUISITES_DIR + '/*', INSTALL_PREFIX])


copy_tree(CFG.PREREQUISITES_DIR, INSTALL_PREFIX, preserve_symlinks=1)

INSTALL_PREFIX_UP = dirname(INSTALL_PREFIX)

os.chdir(INSTALL_PREFIX_UP)

datestamp = '{:%Y%m%d}'.format(datetime.datetime.now())

cc3d_archive_name = 'CC3D_{installer_version_str}_{datestamp}.zip'.format(installer_version_str=installer_version_str,
                                                                          datestamp=datestamp)

cc3d_archive_abspath = join(INSTALL_PREFIX_UP, cc3d_archive_name)
if isfile(cc3d_archive_abspath):
    os.remove(cc3d_archive_abspath)

subprocess.call(['ditto', '-c', '-k', '--keepParent', '-rsrcFork', INSTALL_PREFIX, cc3d_archive_name])
# rm -f ${CC3D_ARCHIVE}
# run_and_watch_status ZIPPING_BINARY ditto -c -k --keepParent -rsrcFork $INSTALL_PREFIX ${CC3D_ARCHIVE}

################### END OF BUILDING ZIP-BASED INSTALLER

os.chdir(CURRENT_DIR)
