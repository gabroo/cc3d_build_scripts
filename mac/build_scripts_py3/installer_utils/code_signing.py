from os.path import *
import os
from argparse import ArgumentParser
from os import walk


def process_cml():
    parser = ArgumentParser()
    parser.add_argument("--input-dir", type=str, help="CC3D installation directory", required=True)
    parser.add_argument("--certificate-label", type=str, help="Signing Certificate Label", required=True)

    args = parser.parse_args()

    return args


def is_exe(fpath):
    return os.path.isfile(fpath) and os.access(fpath, os.X_OK)


def needs_signing(fpath):
    extensions_to_sign = ['.pyd', '.so', '.dylib']
    core, ext = splitext(fpath)
    if ext in extensions_to_sign:
        return True
    if is_exe(fpath):
        return True
    return False


def sign_executable_files(input_dir, certificate_label):
    # counter = 0
    for (dirpath, dirnames, filenames) in walk(input_dir):
        for fname in filenames:
            full_path = join(dirpath, fname)
            if needs_signing(full_path):
                print(f'Executable: {full_path}')
                os.system(f'codesign -s "{certificate_label}" {full_path} --options=runtime --timestamp')
                # counter += 1
                # if counter > 20:
                #     raise StopIteration


def main():
    """

    :return:
    """
    args = process_cml()
    input_dir = args.input_dir
    certificate_label = args.certificate_label

    sign_executable_files(input_dir=input_dir, certificate_label=certificate_label)


if __name__ == '__main__':
    main()
