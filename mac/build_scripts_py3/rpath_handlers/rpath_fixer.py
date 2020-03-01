"""
You run this script after you ran rpath_printout.py where you find which dependent library paths are hard-coded

Example command line may look like this

python rpath_fixer.py --directory=/Users/m/mini_cc3d_install_1 --extensions .dylib .so --target-location-of-hardcoded-libs=/Users/m/mini_cc3d_install_1/lib/site-packages/cc3d/cpp/lib --hardcoded-paths-list /usr/local/Cellar/gcc48/4.8.2/lib/gcc/x86_64-apple-darwin13.0.2/4.8.2/libgcc_s.1.dylib /usr/local/lib/gcc/x86_64-apple-darwin13.0.2/4.8.2/libstdc++.6.dylib

Note , the list of hardcoded paths comes from running rpath_printout.py

"""
import argparse
import os
from os.path import *
from pathlib import Path
import subprocess
import numpy as np


def process_cml():
    parser = argparse.ArgumentParser()

    parser.add_argument('--directory', required=True, type=str)
    parser.add_argument('--extensions', nargs='+', required=True)
    parser.add_argument('--target-location-of-hardcoded-libs', required=True)
    parser.add_argument('--hardcoded-paths-list', nargs='+', required=True)

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


def path_difference(path_a, path_b):
    """
    COmputer relative difference between two paths i.e. a relative path from directory of path_a to path_b
    :param path_a:
    :param path_b:
    :return:
    """
    path_a_parts = Path(path_a).parts
    if isfile(path_a):
        path_a_parts = Path(path_a).parts[:-1]

    if not isdir(path_b):
        raise ValueError ('path_b needs to be a directory')
    path_b_parts = Path(path_b).parts

    array_size = max(len(path_a_parts), len(path_b_parts))

    path_a_array = np.zeros(array_size, dtype='S2048')
    path_b_array = np.zeros(array_size, dtype='S2048')
    path_a_array[:len(path_a_parts)] = path_a_parts[:]
    path_b_array[:len(path_b_parts)] = path_b_parts[:]

    mask = path_a_array == path_b_array

    if len(path_a_parts)< len(path_b_parts):
        print
        anchor_position = sum(mask)
        relative_path = join(*path_b_parts[anchor_position:])
        print('relative_path=', relative_path )
    elif len(path_a_parts) == len(path_b_parts):
        relative_path = ''
    else:
        relative_path = '/'.join(['..']*sum(~mask))

    return relative_path


def fix_single_library(lib_path, hardcoded_paths, target_location_of_hardcoded_libs):
    """

    :param lib_path:
    :param hardcoded_paths:
    :param target_location_of_hardcoded_libs:
    :return:
    """

    print('path_difference')

    relative_path = path_difference(path_a=lib_path, path_b=target_location_of_hardcoded_libs)
    relative_loader_path =f'@loader_path/{relative_path}'
    cmd_add_rpath = f'install_name_tool -add_rpath {relative_loader_path} {lib_path}'
    print('cmd_add_rpath=', cmd_add_rpath)

    os.system(cmd_add_rpath)

    for hard_path in hardcoded_paths:
        base_name_lib_path = basename(hard_path)
        cmd = f'install_name_tool -change {hard_path} @rpath/{base_name_lib_path} {lib_path}'
        print('change rpath cmd=', cmd)
        os.system(cmd)


def fix_hardcoded_paths(directory, extensions, target_location_of_hardcoded_libs, hardcoded_paths_list):
    """

    :param directory:
    :param extensions:
    :return:
    """
    hardcoded_paths = set()

    hardcoded_paths_to_consider = {*hardcoded_paths_list}

    # traverse root directory, and list directories as dirs and files as files
    for root, dirs, files in os.walk(directory):

        path = root.split(os.sep)
        # print((len(path) - 1) * '---', os.path.basename(root))
        for file in files:
            stem, ext = splitext(file)
            if ext in extensions:
                fname = join(root, file)
                print(fname)

                print(len(path) * '---', file)
                cmd_list = ['otool', '-L', f'{fname}']
                result = subprocess.run(cmd_list, stdout=subprocess.PIPE)
                output = result.stdout.decode('utf-8')
                print('This is output')
                local_hardcoded_paths = parse_dependent_otool_output(output=output)

                hard_coded_paths_to_fix = hardcoded_paths_to_consider & local_hardcoded_paths

                fix_single_library(lib_path=fname, hardcoded_paths=hard_coded_paths_to_fix,
                                   target_location_of_hardcoded_libs=target_location_of_hardcoded_libs)

                hardcoded_paths |= local_hardcoded_paths
                print(output)
                # cmd = f'otool -L {fname}'
                # os.system(cmd)

    print('Found the following hardcoded paths')
    for p in hardcoded_paths:
        print(p)


def main():
    args = process_cml()
    directory = args.directory

    extensions = args.extensions
    target_location_of_hardcoded_libs = args.target_location_of_hardcoded_libs
    hardcoded_paths_list = args.hardcoded_paths_list

    fix_hardcoded_paths(directory=directory, extensions=extensions,
                        target_location_of_hardcoded_libs=target_location_of_hardcoded_libs,
                        hardcoded_paths_list=hardcoded_paths_list)


if __name__ == '__main__':
    main()
