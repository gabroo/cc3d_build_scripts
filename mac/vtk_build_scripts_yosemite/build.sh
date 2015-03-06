#!/bin/bash

# ./build.sh --prefix=/Users/mswat/libs/VTK-6.2.0_script_build --source-root=/Users/mswat/Downloads/VTK-6.2.0/ --python-root=/Users/mswat/miniconda/envs/pyqt5 --cores=16

export PREFIX=/usr/local/vtk
export SOURCE_ROOT=/usr/local/vtk
export SYS_PREFIX=/usr
export PYTHON_ROOT=/Users/mswat/miniconda/envs/pyqt5

current_directory=$(pwd)


for i in "$@"
do
case $i in
    -p=*|--prefix=*)
    PREFIX=`echo $i | sed 's/[-a-zA-Z0-9]*=//'`

    ;;
    -s=*|--source-root=*)
    SOURCE_ROOT=`echo $i | sed 's/[-a-zA-Z0-9]*=//'`
    ;;
    
    -y=*|--python-root=*)
    PYTHON_ROOT=`echo $i | sed 's/[-a-zA-Z0-9]*=//'`
    ;;
		
    -c=*|--cores=*)
    MAKE_MULTICORE=`echo $i | sed 's/[-a-zA-Z0-9]*=//'`
    ;;
	    --help)
    
    echo "build_vtk.sh <OPTIONS>"
    echo
    echo "OPTIONS:"
    echo
    echo "-p=<dir> | --prefix=<dir> : vtk installation prefix (target directory) | default /usr/local/vtk"
    echo
    echo "-s=<dir> | --source_root=<dir> : root directory of  vtk source code - default /usr/local/vtk"
    echo
    ;;
    
    *)
            # unknown option
    ;;
esac
done



MAKE_MULTICORE_OPTION=-j$MAKE_MULTICORE


if [ `uname` == Linux ]; then
    CC=gcc44
    CXX=g++44
    CMAKE=cmake
    PY_LIB="libpython2.7.so"
fi
if [ `uname` == Darwin ]; then
    CC=cc
    CXX=c++
    CMAKE=$SYS_PREFIX/bin/cmake
    PY_LIB="libpython2.7.dylib"
    # export DYLD_LIBRARY_PATH=$PREFIX/lib
fi

cd $SOURCE_ROOT
pwd

mkdir build1
cd build1

$CMAKE \
    -DCMAKE_INSTALL_PREFIX:PATH="$PREFIX" \
    -DBUILD_TESTING:BOOL=OFF \
    -DBUILD_EXAMPLES:BOOL=OFF \
    -DBUILD_SHARED_LIBS:BOOL=ON \
    -DPYTHON_EXECUTABLE:FILEPATH=$PYTHON_ROOT/bin/python \
    -DPYTHON_INCLUDE_PATH:PATH=$PYTHON_ROOT/include/python2.7 \
    -DPYTHON_LIBRARY:FILEPATH=$PYTHON_ROOT/lib/$PY_LIB \
    -DVTK_USE_X:BOOL=OFF \
    -DVTK_WRAP_PYTHON:BOOL=ON \
    -DVTK_USE_OFFSCREEN:BOOL=ON \
    ..

echo $MAKE_MULTICORE_OPTION

make $MAKE_MULTICORE_OPTION
make install

cd $current_directory

if [ `uname` == Linux ]; then
    mv $PREFIX/lib/vtk-5.10/lib* $PREFIX/lib
    $REPLACE '/lib/vtk-5.10/lib' '/lib/lib' \
	     $PREFIX/lib/vtk-5.10/VTKTargets-debug.cmake
fi

if [ `uname` == Darwin ]; then
	python osx_vtk_link_fix.py --prefix=$PREFIX
	mkdir $PYTHON_ROOT/lib/vtk-6.2
	cp -R $PREFIX/lib/*.dylib $PYTHON_ROOT/lib/vtk-6.2
	cp -R $PREFIX/lib/python2.7/site-packages/vtk $PYTHON_ROOT/lib/python2.7/site-packages/ 	
fi
