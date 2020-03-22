from recursive_code_sign import codesign_directory_entitlement
from os.path import *

python_install_dir = '/Users/m/miniconda3/envs/roadrunner/lib/python3.7/site-packages'
entitlement_file = '/Users/m/CC3D_BUILD_SCRIPTS_GIT/mac/build_scripts_py3/rpath_handlers/roadrunner_fixes/entitlements.plist'
# python_install_dir = '/Users/m/prerequisites/cc3d_2021'
sub_dirs_to_sign = ['roadrunner']
certificate_label = "Developer ID Application: Indiana University (5J69S77A7G)"
keychain_path = "/Users/m/Library/Keychains/login.keychain-db"


for sub_dir in sub_dirs_to_sign:
    directory = join(python_install_dir, sub_dir)
    codesign_directory_rr(
        directory=directory, certificate_label=certificate_label, keychain_path=keychain_path,
        entitlement_file=entitlement_file

    )


"""
To check entitlements in a binary use this (example):

codesign -d --entitlements :- /Users/m/miniconda3/envs/roadrunner/lib/python3.7/site-packages/roadrunner/libroadrunner.1.6.0.dylib

"""