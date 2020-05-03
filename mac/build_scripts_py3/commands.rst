to compile run the following:

.. code-block:: console

    conda activate cc3d_2021
    export PYTHONPATH=/Users/m/CC3D_BUILD_SCRIPTS_GIT/
    cd CC3D_BUILD_SCRIPTS_GIT/
    python /Users/m/CC3D_BUILD_SCRIPTS_GIT/mac/build_scripts_py3/build_script_dmg_10.14.py -p /Users/m/install_projects/CC3D_4.2.0 -s /Users/m/CC3D_PY3_GIT   -v 4.2.0.0 --config=mac/build_scripts_py3/config_64bit_2021_10.14.json -c 8
    python /Users/m/CC3D_BUILD_SCRIPTS_GIT/mac/build_scripts_py3/rpath_handlers/finalize_cc3d_install.py --cc3d-install-dir=/Users/m/install_projects/CC3D_4.2.0 --certificate-label="Developer ID Application: Indiana University (5J69S77A7G)" --python-source-signed-dir=/Users/m/prerequisites/4.1.2_10.14/python37_signed_entitlements --keychain-path=/Users/m/Library/Keychains/login.keychain-db