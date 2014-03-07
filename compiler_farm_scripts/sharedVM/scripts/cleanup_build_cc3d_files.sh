#!/bin/bash
export VERSION=3.7.0
export VERSION1=3.7.1
export VERSION2=3.7.2
export VERSION3=RR_LLVM
echo "THIS IS VERSION ${VERSION} "


export CC3D_GIT_DIR=~/CC3D_GIT
export CC3D_BINARIES_DIR=/media/sf_sharedVM/binaries/${VERSION}/linux
eval CC3D_GIT_DIR=$CC3D_GIT_DIR
export number_of_cpus=8
export install_path=~/install_projects_${VERSION}/${VERSION}
eval install_path=$install_path


rm -rf ~/install_projects_${VERSION}
rm -rf ~/install_projects_${VERSION1}
rm -rf ~/install_projects_${VERSION2}
rm -rf ~/install_projects_${VERSION3}