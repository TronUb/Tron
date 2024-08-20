@echo off
setlocal

:: File containing the list of required packages
set REQUIREMENTS_FILE=requirements.txt
set INSTALLED_FILE=installed_dependencies.txt

:: Main function
:main
:: Show message
echo Running script, please be patient ...

:: Check Python 3 installation
echo Checking python installation ...
where python3 >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python3 is not installed. Trying to install Python3 ...
    echo Please install Python3 manually from the Python website or using a package manager.
    echo Exiting script with error.
    exit /b 1
)

:: Check and install userbot dependencies
if not exist "%REQUIREMENTS_FILE%" (
    echo REQUIREMENTS_FILE file not found, Exiting script with error.
    exit /b 1
)

echo Checking userbot dependencies ...
for /f "usebackq tokens=* delims=" %%i in ("%REQUIREMENTS_FILE%") do (
    :: Skip empty lines and comments
    if "%%i"=="" goto :eof
    if "%%i"=="REM" goto :eof

    :: Check if the package is installed
    pip show %%i >nul 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo %%i is not installed, trying to install ...
        pip install %%i
    ) else (
        echo %%i >> "%INSTALLED_FILE%"
    )
)

:: Run userbot
cls
python3 -m main
echo Configuring Userbot, wait ....
if %ERRORLEVEL% NEQ 0 (
    echo Failed to run userbot. Exiting script with error.
    exit /b 1
)
endlocal
