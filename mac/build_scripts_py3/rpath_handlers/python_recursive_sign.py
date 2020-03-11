from recursive_code_sign import codesign_directory
from os.path import *

python_install_dir = '/Users/m/prerequisites/4.1.2/python37'
# python_install_dir = '/Users/m/prerequisites/cc3d_2021'
sub_dirs_to_sign = ['bin', 'lib', 'libexec', 'plugins', 'qml', 'sbin', 'share/cmake-3.16']
certificate_label = "Developer ID Application: Indiana University (5J69S77A7G)"
keychain_path = "/Users/m/Library/Keychains/login.keychain-db"


for sub_dir in sub_dirs_to_sign:
    directory = join(python_install_dir, sub_dir)
    codesign_directory(directory=directory, certificate_label=certificate_label, keychain_path=keychain_path)
