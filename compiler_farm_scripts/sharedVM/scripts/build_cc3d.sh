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

export CC3D_BUILD_SCRIPTS_GIT_DIR=~/CC3D_BUILD_SCRIPTS_GIT_DIR
eval CC3D_BUILD_SCRIPTS_GIT_DIR=$CC3D_BUILD_SCRIPTS_GIT_DIR

time run_and_watch_status BUILDING_CC3D_370 ${CC3D_BUILD_SCRIPTS_GIT_DIR}/build-cc3d-370-compiler-farm.sh
time run_and_watch_status BUILDING_RR_LLVM  ${CC3D_BUILD_SCRIPTS_GIT_DIR}/build-rr-llvm-compiler-farm.sh 
time run_and_watch_status BUILDING_CC3D_371 ${CC3D_BUILD_SCRIPTS_GIT_DIR}/build-cc3d-371-compiler-farm.sh
/sbin/poweroff


