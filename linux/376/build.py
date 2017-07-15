"""
This script runs on linux and builds cc3d .

Requirements:
1. conda must be installed -  use Miniconda installer for Python 2.7 for 64-bit linux
    https://conda.io/miniconda.html
2. swig
3.  gcc/g++ compiler
4. git


example command:

    python build.py --prefix=/home/m/376_auto --source-root=/home/m/CC3D_GIT --build-dir=/home/m/376_auto_build --version=3.7.6 --cores=2

For help on command line options type:

    oython build.py --help

"""
import argparse
import sys
import os
from os.path import *
from subprocess import Popen, PIPE
import subprocess
import argparse
from functools import partial


def run_command(command_input, check_command_status=True):
    """

    :param command_input: {string or list}
    :return:
    """
    if isinstance(command_input, basestring):
        command_str_list = command_input.split(' ')
        command_str_list = [e for e in command_str_list if e not in [' ', '']]  # removing empty entries
    else:
        command_str_list = command_input
    if check_command_status:
        subprocess.call(command_str_list)
        return None, None, None

    else:
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



if __name__ == '__main__':

    cml_parser = argparse.ArgumentParser()

    cml_parser.add_argument("-p", "--prefix", action="store", help="CC3D installation directory")
    cml_parser.add_argument("-s", "--source-root", action="store", help="CC3D GIT Repository")
    cml_parser.add_argument("-b", "--build-dir", action="store", help="build directory")
    cml_parser.add_argument("-v", "--version", action="store", help="version string", default='3.7.6')
    cml_parser.add_argument("-c", "--cores", action="store", help="number of cpu cores", type=int, default=2)
    cml_parser.add_argument("-d", "--dependency-channel", action="store", help="name of  conda dependency channel",
                            default='compucell3d')
    cml_parser.add_argument("-e", "--conda-env-name", action="store", help="name of conda environment to create",
                            default='cc3d_test_15')
    cml_args = cml_parser.parse_args()

    conda_env = cml_args.conda_env_name
    conda_dependency_channel = cml_args.dependency_channel
    conda_dependencies = 'qscintilla2 pyqtgraph webcolors jinja2 scipy vtk=6.3.0 pyzmq'
    install_prefix = cml_args.prefix
    CC3D_SOURCE_PATH = join(cml_args.source_root, 'CompuCell3D')
    CC3D_BUILD_PATH = cml_args.build_dir

    # CC3D_SOURCE_PATH = '/home/m/CC3D_GIT/CompuCell3D'
    # CC3D_BUILD_PATH = '/home/m/install_projects/demo'
    num_cpus = cml_args.cores
    try:
        MAJOR_VERSION, MINOR_VERSION, BUILD_VERSION = map(int, cml_args.version.split('.'))
    except:
        print ('Version string must have the following format int.int.int e.g. 3.7.6')
        sys.exit()

    rc_check_status = partial(run_command, check_command_status=False)
    rc = partial(run_command, check_command_status=True)

    output, err, ret_code = rc_check_status('which conda')
    if not output:
        print 'Could not locate conda. Make sure it is in your path'
        sys.exit(1)
    conda_exec = abspath(output.strip())
    conda_path = dirname(dirname(conda_exec))

    output, err, ret_code = rc_check_status('which cmake')
    if not output:
        print 'Could not locate conda. Make sure it is in your path'
        sys.exit(1)
    cmake_path = abspath(output.strip())

    output, err, ret_code = rc('conda create -n {conda_env} python'.format(conda_env=conda_env))

    command = 'conda install -n {conda_env} -c {conda_channel} {dependencies} '.format(dependencies=conda_dependencies,
                                                                                       conda_channel=conda_dependency_channel,
                                                                                       conda_env=conda_env)

    output, err, ret_code = rc(
        'conda install -y -n {conda_env} -c {conda_channel} {dependencies} '.format(dependencies=conda_dependencies,
                                                                                 conda_channel=conda_dependency_channel,
                                                                                 conda_env=conda_env))

    PYTHON_EXECUTABLE = join(conda_path, 'envs', conda_env, 'bin', 'python')
    PYTHON_INCLUDE_DIR = join(conda_path, 'envs', conda_env, 'include/python2.7')
    PYTHON_LIBRARY = join(conda_path, 'envs', conda_env, 'lib/libpython2.7.so')
    VTK_DIR = join(conda_path, 'envs', conda_env, 'lib/cmake/vtk-6.3')

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

    rc(cmake_config_command)
    rc(['make', '-j', '{num_cpus}'.format(num_cpus=num_cpus), 'install'])


    # subprocess.call(cmake_config_command)
    #
    # subprocess.call(['make', '-j', '{num_cpus}'.format(num_cpus=num_cpus), 'install'])
