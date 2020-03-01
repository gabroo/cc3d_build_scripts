"""
https://stackoverflow.com/questions/49748988/how-to-codesign-dmg-and-app-inside-it
This code helps with recursive code-signing of all files in a given directory

Example command line may look like this

python recursive_code_sign.py --directory=/Users/m/mini_cc3d_install_1/
--certificate-label="Developer ID Application: Indiana University (XXX)"
--keychain-path=/Users/m/Library/Keychains/login.keychain-db


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
    parser.add_argument('--certificate-label', required=True, type=str)
    parser.add_argument('--keychain-path', required=True)

    args = parser.parse_args()

    return args


def codesign_directory(directory, certificate_label, keychain_path):
    """

    :param directory:
    :param certificate_label:
    :param keychain_path:
    :return:
    """

    # traverse root directory, and list directories as dirs and files as files
    for root, dirs, files in os.walk(directory):

        path = root.split(os.sep)
        for file in files:
            stem, ext = splitext(file)

            fname = join(root, file)
            print(fname)
            cmd = f'codesign -f -v -s "{certificate_label}" --keychain {keychain_path} {fname}'
            os.system(cmd)


def main():
    args = process_cml()
    directory = args.directory

    certificate_label = args.certificate_label
    keychain_path = args.keychain_path

    codesign_directory(directory=directory, certificate_label=certificate_label, keychain_path=keychain_path)


if __name__ == '__main__':
    main()
