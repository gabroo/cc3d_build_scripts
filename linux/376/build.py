import argparse
import sys
import os
from os.path import *
from subprocess import Popen, PIPE
import subprocess

conda_env = 'cc3d_test_11'
conda_dependency_channel = 'compucell3d'
conda_dependencies = 'qscintilla2 pyqtgraph webcolors jinja2 scipy vtk=6.3.0'
install_prefix = '/home/m/376_demo'
CC3D_SOURCE_PATH = '/home/m/CC3D_GIT/CompuCell3D'
CC3D_BUILD_PATH = '/home/m/install_projects/demo'
num_cpus = 2
MAJOR_VERSION = 3
MINOR_VERSION = 7
BUILD_VERSION = 6



def run_command(command_input):
    """

    :param command_input: {string or list}
    :return:
    """
    if isinstance(command_input,basestring):
        command_str_list = command_input.split(' ')
        command_str_list = [e for e in command_str_list if e not in [' ', '']]  # removing empty entries
    else:
        command_str_list = command_input

    p = Popen(command_str_list, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate(b"input data that is passed to subprocess' stdin")
    ret_code = p.returncode
    print 'output:'
    print output
    print 'err:'
    print err
    print 'ret_code:'
    print ret_code
    return output, err, ret_code


rc = run_command

print

output, err, ret_code = rc('which conda')
if not output:
    print 'Could not locate conda. Make sure it is in your path'
    sys.exit(1)
conda_exec = abspath(output.strip())
conda_path = dirname(dirname(conda_exec))


output, err, ret_code = rc('which cmake')
if not output:
    print 'Could not locate conda. Make sure it is in your path'
    sys.exit(1)
cmake_path = abspath(output.strip())


output, err, ret_code = rc('conda create -n {conda_env} python'.format(conda_env=conda_env))

command = 'conda install -n {conda_env} -c {conda_channel} {dependencies} '.format(dependencies=conda_dependencies,
                                                                             conda_channel=conda_dependency_channel,
                                                                             conda_env=conda_env)

output, err, ret_code = rc(
    'conda install -n {conda_env} -c {conda_channel} {dependencies} '.format(dependencies=conda_dependencies,
                                                                             conda_channel=conda_dependency_channel,
                                                                             conda_env=conda_env))

PYTHON_EXECUTABLE = join(conda_path,'envs',conda_env,'bin','python')
PYTHON_INCLUDE_DIR = join(conda_path,'envs',conda_env,'include/python2.7')
PYTHON_LIBRARY = join(conda_path,'envs',conda_env,'lib/libpython2.7.so')
VTK_DIR = join(conda_path,'envs',conda_env,'lib/cmake/vtk-6.3')

PYQT_VERSION = 5


cmake_config_command = [cmake_path, '-G', 'Unix Makefiles', '-DCMAKE_BUILD_TYPE:STRING=Release',
                     '-DNO_OPENCL:BOOLEAN=ON',
                     '-DCMAKE_INSTALL_PREFIX:PATH=' + install_prefix,
                     '-DCOMPUCELL3D_A_MAJOR_VERSION:STRING=' + str(MAJOR_VERSION),
                     '-DCOMPUCELL3D_B_MINOR_VERSION:STRING=' + str(MINOR_VERSION),
                     '-DCOMPUCELL3D_C_BUILD_VERSION:STRING=' + str(BUILD_VERSION),
                     '-DPYTHON_EXECUTABLE=' + PYTHON_EXECUTABLE, '-DPYTHON_INCLUDE_DIR=' + PYTHON_INCLUDE_DIR,
                     '-DPYTHON_LIBRARY=' + PYTHON_LIBRARY,
                     '-DVTK_DIR=' + VTK_DIR,
                     '-DPYQT_VERSION:STRING=' + str(PYQT_VERSION),
                      CC3D_SOURCE_PATH]

try:
    os.makedirs(CC3D_BUILD_PATH)
except OSError as e:
    if 'File exists' in str(e):
        pass

os.chdir(CC3D_BUILD_PATH)

subprocess.call(cmake_config_command)

subprocess.call(['make','-j', '{num_cpus}'.format(num_cpus=num_cpus), 'install'])


