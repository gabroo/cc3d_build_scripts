# example command ./generate-xcode-proj-mavericks.sh -s=~/CC3D_GIT 
#command line parsing

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
        exit
    fi
    return $status    

}

current_directory=$(pwd)

export MAJOR_VERSION=3
export MINOR_VERSION=7
export BUILD_VERSION=1

export PYTHON_MINOR_VERSION=7

export VERSION=${MAJOR_VERSION}.${MINOR_VERSION}.${BUILD_VERSION}
echo "THIS IS VERSION ${VERSION} "


export BUILD_ROOT=
export SOURCE_ROOT=~/CC3D_GIT
export DEPENDENCIES_ROOT=
export INSTALL_PREFIX=~/install_projects/CC3D_3.7.1
export RR_SOURCE_ROOT=~/RR_OSX
#mac variables
export GCC_DIR=/usr/local/Cellar/gcc48/4.8.2/
export VTK_BIN_AND_BUILD_DIR=/Users/Shared/vtk-5.10.1
export MAC_DEPS=/Users/Shared/CC3Ddev/Dependencies/
# export OUTPUT_BINARY_NAME=CC3D_3.7.1_MacOSX_10.8

export OUTPUT_BINARY_NAME=CC3D_${MAJOR_VERSION}.${MINOR_VERSION}.${BUILD_VERSION}_MacOSX_10.9

export RR_INSTALL_PATH=/Users/Shared/RR_LLVM_install

export BUILD_CC3D=NO
export BUILD_BIONET=NO
export BUILD_BIONET_DEPEND=NO
export BUILD_CELLDRAW=NO
export BUILD_RR=NO
export BUILD_RR_DEPEND=NO
export BUILD_ALL=YES
export MAKE_MULTICORE=1



for i in "$@"
do
case $i in
    -p=*|--prefix=*)
    INSTALL_PREFIX=`echo $i | sed 's/[-a-zA-Z0-9]*=//'`

    ;;
    -s=*|--source-root=*)
    SOURCE_ROOT=`echo $i | sed 's/[-a-zA-Z0-9]*=//'`
    ;;

    -r=*|--rr-source-root=*)
    RR_SOURCE_ROOT=`echo $i | sed 's/[-a-zA-Z0-9]*=//'`
    ;;

    -d=*|--mac-dependencies=*)
    MAC_DEPS=`echo $i | sed 's/[-a-zA-Z0-9]*=//'`
    ;;
    -b=*|--output-binary-name=*)
    OUTPUT_BINARY_NAME=`echo $i | sed 's/[-a-zA-Z0-9]*=//'`
    ;;

    
    -c=*|--cores=*)
    MAKE_MULTICORE=`echo $i | sed 's/[-a-zA-Z0-9]*=//'`
    ;;
    --cc3d)
    BUILD_ALL=NO
    BUILD_CC3D=YES
    ;;
    --bionet)
    BUILD_ALL=NO
    BUILD_BIONET=YES
    ;;
    --bionet-depend)
    BUILD_ALL=NO
    BUILD_BIONET_DEPEND=YES
    ;;
    --celldraw)
    BUILD_ALL=NO
    BUILD_CELLDRAW=YES
    ;;
    --rr)
    BUILD_ALL=NO
    BUILD_RR=YES
    ;;
    --rr-depend)
    BUILD_ALL=NO
    BUILD_RR_DEPEND=YES
    ;;
    --help)
    
    echo "build-osx-cc3d.sh <OPTIONS>"
    echo
    echo "OPTIONS:"
    echo
    echo "-p=<dir> | --prefix=<dir> : cc3d installation prefix (target directory) | default ~/install_projects/cc3d"
    echo
    echo "-r=<dir> | --rr-source-root=<dir> : RoadRunner Source"
    echo
    echo "-s=<dir> | --source-root=<dir> : root directory of CC3D GIT repository "
    echo
    echo "specifying options below will allow for selection of specific projects to build."
    echo  "If you are rebuilding CompuCell3D by picking specific projects you will shorten build time"
    echo
    echo "--cc3d : builds CompuCell3D"
    echo
    echo "--bionet : builds BionetSolver"
    echo
    echo "--bionet-depend : builds BionetSolver dependencies"
    echo
    echo "--celldraw : builds celldraw"
    echo
    echo "--rr : builds RoadRunner"
    echo
    echo "--rr-depend : builds RoadRunner dependencies"
    echo
    ;;
    
    *)
            # unknown option
    ;;
esac
done



if [ "$BUILD_ALL" == YES ]
then
  BUILD_CC3D=YES
  BUILD_BIONET=YES
  BUILD_BIONET_DEPEND=YES
  BUILD_CELLDRAW=YES
  BUILD_RR=YES
  BUILD_RR_DEPEND=YES
  BUILD_ALL=YES
fi

echo BUILD_CC3D $BUILD_CC3D
echo BUILD_BIONET $BUILD_BIONET
echo BUILD_BIONET_DEPEND $BUILD_BIONET_DEPEND
echo BUILD_CELLDRAW $BUILD_CELLDRAW
echo BUILD_RR $BUILD_RR_DEPEND
echo BUILD_RR_DEPEND $BUILD_RR_DEPEND


# expanding paths
eval INSTALL_PREFIX=$INSTALL_PREFIX
eval BUILD_ROOT=$BUILD_ROOT
eval SOURCE_ROOT=$SOURCE_ROOT
eval DEPENDENCIES_ROOT=$DEPENDENCIES_ROOT


BUILD_ROOT=${INSTALL_PREFIX}_build
DEPENDENCIES_ROOT=${INSTALL_PREFIX}_depend

echo INSTALL_PREFIX = ${INSTALL_PREFIX}
echo BUILD_ROOT = ${BUILD_ROOT}
echo SOURCE_ROOT = ${SOURCE_ROOT}
echo DEPENDENCIES_ROOT = ${DEPENDENCIES_ROOT}



echo MAKE_MULTICORE= $MAKE_MULTICORE
MAKE_MULTICORE_OPTION=-j$MAKE_MULTICORE
echo OPTION=$MAKE_MULTICORE_OPTION



mkdir -p $BUILD_ROOT
mkdir -p $DEPENDENCIES_ROOT

export BUILD_ROOT=/Users/m/CC3D_GIT_build/CompuCell3D

if [ "$BUILD_CC3D" == YES ]
then
  ############# BUILDING CC3D
  mkdir -p $BUILD_ROOT
  cd $BUILD_ROOT

  run_and_watch_status COMPUCELL3D_CMAKE_CONFIG cmake -G "Xcode" -DPYTHON_MINOR_VERSION:STRING=${PYTHON_MINOR_VERSION} -DCMAKE_INSTALL_PREFIX:PATH=$INSTALL_PREFIX -DCOMPUCELL3D_A_MAJOR_VERSION:STRING=$MAJOR_VERSION -DCOMPUCELL3D_B_MINOR_VERSION:STRING=$MINOR_VERSION -DCOMPUCELL3D_C_MAJOR_BUILD:STRING=$BUILD_VERSION -DCMAKE_OSX_DEPLOYMENT_TARGET:STRING=10.9 -DPYTHON_EXECUTABLE:FILEPATH=/usr/bin/python2.${PYTHON_MINOR_VERSION} -DPYTHON_INCLUDE_DIR:PATH=/System/Library/Frameworks/Python.framework/Versions/2.${PYTHON_MINOR_VERSION}/Headers -DEIGEN3_INCLUDE_DIR=${SOURCE_ROOT}/CompuCell3D/core/Eigen -DPYTHON_LIBRARY:FILEPATH=/usr/lib/libpython2.${PYTHON_MINOR_VERSION}.dylib -DCMAKE_C_COMPILER:FILEPATH=${GCC_DIR}/bin/gcc -DCMAKE_CXX_COMPILER:FILEPATH=${GCC_DIR}/bin/g++ PATH=$INSTALL_PREFIX  -DVTK_DIR:PATH=${VTK_BIN_AND_BUILD_DIR}/lib/vtk-5.10 -DCMAKE_CXX_FLAGS="-mmacosx-version-min=10.6 -O3 -g -fpermissive -m64" -DCMAKE_C_FLAGS="-mmacosx-version-min=10.6 -O3 -g -fpermissive -m64" $SOURCE_ROOT/CompuCell3D
#   run_and_watch_status COMPUCELL3D_COMPILE_AND_INSTALL make $MAKE_MULTICORE_OPTION  && make install
  
  ############# END OF BUILDING CC3D
fi
