from recursive_code_sign import codesign_directory_entitlement
from recursive_code_sign import codesign_directory
from os.path import *

python_install_dir = '/Users/m/miniconda3/envs/roadrunner'
# python_install_dir = '/Users/m/miniconda3/envs/rr1'
entitlement_file = '/Users/m/CC3D_BUILD_SCRIPTS_GIT/mac/build_scripts_py3/rpath_handlers/roadrunner_fixes/entitlements.plist'
# python_install_dir = '/Users/m/prerequisites/cc3d_2021'
sub_dirs_to_sign = ['bin', 'lib', 'libexec', 'plugins', 'qml', 'sbin', 'share/cmake-3.16',
                    'compucell3d.app', 'twedit++.app','python.app', 'Contents']
certificate_label = "Developer ID Application: Indiana University (5J69S77A7G)"
keychain_path = "/Users/m/Library/Keychains/login.keychain-db"


for sub_dir in sub_dirs_to_sign:
    directory = join(python_install_dir, sub_dir)
    # codesign_directory(directory=directory, certificate_label=certificate_label, keychain_path=keychain_path
    #                       )

    codesign_directory_entitlement(directory=directory, certificate_label=certificate_label, keychain_path=keychain_path,
                          entitlement_file=entitlement_file
                          )
