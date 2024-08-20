@echo off
setlocal

:: File containing the list of required packages
set "REQUIREMENTS_FILE=requirements.txt"
set "INSTALLED_FILE=installed_dependencies.txt"

:: Main function
:main
:: Show message
echo Running script, please be patient ...

:: Check if winget is available
where winget >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo winget is not installed. Please install it first.
    exit /b 1
)

:: Check if Scoop is already installed
echo Checking for Scoop installation...
winget list scoop >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Scoop is already installed.
) else (
    :: Install Scoop using winget
    echo Installing Scoop...
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
    Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression

    :: Check if Scoop was installed successfully
    if %ERRORLEVEL% NEQ 0 (
        echo There was an issue installing Scoop.
        exit /b 1
    )
)

:: Install ffmpeg using Scoop
echo Installing ffmpeg ...
scoop install ffmpeg
if %ERRORLEVEL% NEQ 0 (
    echo There was an issue installing ffmpeg.
    exit /b 1
)

:: Check Python 3 installation
echo Checking python installation ...
where python3 >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python3 is not installed. Please install Python3 manually from the Python website or using a package manager.
    echo Exiting script with error.
    exit /b 1
)

:: Check and install userbot dependencies
if not exist "%REQUIREMENTS_FILE%" (
    echo %REQUIREMENTS_FILE% file not found, Exiting script with error.
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

        :: Handle special cases for certain packages
        if "%%i"=="lxml" (
            scoop install libxml2
            scoop install libxslt
            pip install lxml
        ) else if "%%i"=="psycopg2" (
            scoop install postgresql python make clang
            pip install psycopg2
        ) else if "%%i"=="pillow" (
            scoop install libjpeg-turbo
            pip install pillow
        ) else (
            pip install %%i
        )
    ) else (
        echo %%i >> "%INSTALLED_FILE%"
    )
)

:: Run userbot
cls
echo Running userbot...
python3 -m main
if %ERRORLEVEL% NEQ 0 (
    echo Failed to run userbot. Exiting script with error.
    exit /b 1
)

echo Userbot configured successfully.
endlocal
exit /b 0
