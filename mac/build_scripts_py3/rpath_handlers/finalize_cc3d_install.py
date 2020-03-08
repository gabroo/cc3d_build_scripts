"""
You run this script to finalize installation of signed version of cc3d

example command:

python finalize_cc3d_install.py
--cc3d-install-dir=/Volumes/mavericksosx/Users/m/install_projects/CC3D_4.1.2
--certificate-label="Developer ID Application: Indiana University (5J69S77A7G)"
--python-source-signed-dir=/Users/m/prerequisites/4.1.2/python37_signed
--keychain-path=/Users/m/Library/Keychains/login.keychain-db

"""
from recursive_code_sign import codesign_directory
from pathlib import Path
from distutils.dir_util import copy_tree
from os.path import *
import argparse


def process_cml():
    parser = argparse.ArgumentParser()

    parser.add_argument('--cc3d-install-dir', required=True, type=str)
    parser.add_argument('--certificate-label', required=True, type=str)
    parser.add_argument('--python-source-signed-dir', required=True, type=str)
    parser.add_argument('--keychain-path', required=True)

    args = parser.parse_args()

    return args


def main():
    """

    :return:
    """

    args = process_cml()
    python_source_signed_dir = args.python_source_signed_dir
    cc3d_install_dir = args.cc3d_install_dir
    certificate_label = args.certificate_label
    keychain_path = args.keychain_path

    codesign_directory(directory=cc3d_install_dir, certificate_label=certificate_label, keychain_path=keychain_path)

    python_target_install_dir = join(cc3d_install_dir, 'python37')
    Path(python_target_install_dir).mkdir(parents=True, exist_ok=True)

    try:
        copy_tree(python_source_signed_dir, python_target_install_dir, preserve_symlinks=1)
    except OSError as e:
        if str(e).find('File exists'):
            pass
        else:
            raise e


if __name__ == '__main__':
    main()
