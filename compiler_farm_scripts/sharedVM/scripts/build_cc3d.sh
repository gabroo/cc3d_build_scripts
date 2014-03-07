#!/bin/bash

function run_and_watch_status {
    # first argument is a task descriptor and is mandatory
    # the remaining arguments make up a command to execute
    
    #executing the command
    "${@:2}"
    # querrying its status
    status=$?
    echo "STATUS=$status"
    if [ $status -ne 0 ]; then
        echo "error with $1"
        exit $status
    fi
    return $status    

}

########### CLEANUP 
# rm -rf ~/install_project*
# rm -rf CC3D_*
# rm -rf RR_*

# /media/sf_sharedVM/scripts/install_basics.sh
########### CLEANUP 


export CC3D_BUILD_SCRIPTS_GIT_DIR=~/CC3D_BUILD_SCRIPTS_GIT
eval CC3D_BUILD_SCRIPTS_GIT_DIR=$CC3D_BUILD_SCRIPTS_GIT_DIR

cd $CC3D_BUILD_SCRIPTS_GIT_DIR
git pull

# time run_and_watch_status BUILDING_CC3D_370 ${CC3D_BUILD_SCRIPTS_GIT_DIR}/compiler_farm_scripts/sharedVM/scripts/build-cc3d-370-compiler-farm.sh
# time run_and_watch_status BUILDING_RR_LLVM  ${CC3D_BUILD_SCRIPTS_GIT_DIR}/compiler_farm_scripts/sharedVM/scripts/build-rr-llvm-compiler-farm.sh 
# time run_and_watch_status BUILDING_CC3D_371 ${CC3D_BUILD_SCRIPTS_GIT_DIR}/compiler_farm_scripts/sharedVM/scripts/build-cc3d-371-compiler-farm.sh

time run_and_watch_status CLEANING_OLD_PROJECTS ${CC3D_BUILD_SCRIPTS_GIT_DIR}/compiler_farm_scripts/sharedVM/scripts/cleanup_build_cc3d_files.sh

time run_and_watch_status BUILDING_RR_LLVM  ${CC3D_BUILD_SCRIPTS_GIT_DIR}/compiler_farm_scripts/sharedVM/scripts/build-rr-llvm-compiler-farm.sh 
time run_and_watch_status BUILDING_CC3D_372 ${CC3D_BUILD_SCRIPTS_GIT_DIR}/compiler_farm_scripts/sharedVM/scripts/build-cc3d-372-compiler-farm.sh

/sbin/poweroff

