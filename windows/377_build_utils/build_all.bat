
@set CURRENT_DIRECTORY=%CD%

REM call "C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\vcvarsall.bat" x86

REM cd ..\377-32bit
REM c:\miniconda32\python .\win_cc3d_builder_377.py  -p D:/install_projects/3.7.7-32bit -s D:/CC3D_GIT  -i D:/CC3D_FILES_SVN/binaries/3.7.7/windows -v 3.7.7.0

call "C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\vcvarsall.bat" amd64

cd ..\377-64bit
c:\miniconda64\python .\win_cc3d_builder_377.py  -p D:/install_projects/3.7.7-64bit -s D:/CC3D_GIT  -i D:/CC3D_FILES_SVN/binaries/3.7.7/windows -v 3.7.7.0

REM call "C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\vcvarsall.bat" amd64

REM cd ..\377-64bit-gpu
REM c:\miniconda64\python .\win_cc3d_builder_gpu_377.py  -p D:/install_projects/3.7.7-gpu-64bit -s D:/CC3D_GIT  -i D:/CC3D_FILES_SVN/binaries/3.7.7/windows -v 3.7.7.0

cd %CURRENT_DIRECTORY%