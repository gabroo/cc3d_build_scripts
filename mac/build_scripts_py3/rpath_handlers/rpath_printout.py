"""
This script examines which specification of rpath is a hardcoded path. The output of this script is a list of
all hardcoded paths

Example command line may look like this:

python rpath_printout.py --directory=/Users/m/mini_cc3d_install_1 --extensions .dylib .so
"""


import argparse
import os
from os.path import *
from pathlib import Path
import subprocess


def process_cml():
    parser = argparse.ArgumentParser()

    parser.add_argument('--directory', required=True, type=str)
    parser.add_argument('--extensions', nargs='+', required=True)

    args = parser.parse_args()

    return args

def parse_dependent_otool_output(output):
    """

    :return:
    """
    hardcoded_paths = []
    out_list = output.split('\n')

    for i, line in enumerate(out_list):
        if i==0:
            continue
        line = line.strip()
        if line and not line.startswith('@'):
            split_line = line.split(' ')
            hardcoded_paths.append(split_line[0])

    return {*hardcoded_paths}



def identify_hardcoded_paths(directory, extensions):
    """

    :param directory:
    :param extensions:
    :return:
    """
    hardcoded_paths = set()

    # traverse root directory, and list directories as dirs and files as files
    for root, dirs, files in os.walk(directory):


        path = root.split(os.sep)
        # print((len(path) - 1) * '---', os.path.basename(root))
        for file in files:
            stem, ext  = splitext(file)
            if ext in extensions:
                fname = join(root, file)
                print(fname)

                print(len(path) * '---', file)
                cmd_list = ['otool', '-L', f'{fname}']
                result = subprocess.run(cmd_list, stdout=subprocess.PIPE)
                output = result.stdout.decode('utf-8')
                print('This is output')
                local_hardcoded_paths = parse_dependent_otool_output(output=output)

                hardcoded_paths |= local_hardcoded_paths
                print (output)
                # cmd = f'otool -L {fname}'
                # os.system(cmd)

    print ('Found the following hardcoded paths')
    for p in hardcoded_paths:
        print(p)

def main():
    args = process_cml()
    directory = args.directory

    extensions = args.extensions

    identify_hardcoded_paths(directory=directory, extensions=extensions)


if __name__ == '__main__':
    main()