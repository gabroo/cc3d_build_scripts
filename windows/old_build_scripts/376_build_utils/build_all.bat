
@set CURRENT_DIRECTORY=%CD%

call "C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\vcvarsall.bat" x86

cd ..\376-32bit
c:\miniconda32\python .\win_cc3d_builder_376.py  -p D:/install_projects/3.7.6-32bit -s D:/CC3D_GIT  -i D:/CC3D_FILES_SVN/binaries/3.7.6/windows -v 3.7.6.0

call "C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\vcvarsall.bat" amd64

cd ..\376-64bit
c:\miniconda64\python .\win_cc3d_builder_376.py  -p D:/install_projects/3.7.6-64bit -s D:/CC3D_GIT  -i D:/CC3D_FILES_SVN/binaries/3.7.6/windows -v 3.7.6.0

call "C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\vcvarsall.bat" amd64

cd ..\376-64bit-gpu
c:\miniconda64\python .\win_cc3d_builder_gpu_376.py  -p D:/install_projects/3.7.6-gpu-64bit -s D:/CC3D_GIT  -i D:/CC3D_FILES_SVN/binaries/3.7.6/windows -v 3.7.6.0

cd %CURRENT_DIRECTORY%