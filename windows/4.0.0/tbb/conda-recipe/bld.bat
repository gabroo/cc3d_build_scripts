echo "INSIDE BUILD SCRIPT"
xcopy d:\CC3D_BUILD_SCRIPTS_GIT\windows\4.0.0\tbb\tbb_64bit_dist\* "%LIBRARY_PREFIX%" /s /e

REM xcopy c:\tbb_64bit_dist\* %LIBRARY_PREFIX% /s /e
