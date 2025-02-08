@echo off
setlocal

:: Define file paths
set "REQUIREMENTS_FILE=requirements.txt"
set "WHEELHOUSE_DIR=wheelhouse"

:: Check if --skip-ffmpeg argument is passed
set "SKIP_FFMPEG=0"
for %%a in (%*) do (
    if "%%a"=="--skip-ffmpeg" set "SKIP_FFMPEG=1"
)

:: Check if Python is installed
echo Checking Python installation...
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install it manually.
    exit /b 1
)

:: Check if ffmpeg is installed (unless skipped)
if %SKIP_FFMPEG%==0 (
    echo Checking ffmpeg installation...
    where ffmpeg >nul 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo ffmpeg is not installed. Installing via winget...
        winget install ffmpeg
        if %ERRORLEVEL% NEQ 0 (
            echo Failed to install ffmpeg using winget. Please install manually.
            exit /b 1
        )
    )
) else (
    echo Skipping ffmpeg installation as requested.
)

:: Install dependencies from wheelhouse
if not exist "%WHEELHOUSE_DIR%" (
    echo Wheelhouse directory not found. Please ensure dependencies are bundled.
    exit /b 1
)

echo Installing dependencies from wheelhouse...
pip install --no-index --find-links=%WHEELHOUSE_DIR% -r %REQUIREMENTS_FILE%
if %ERRORLEVEL% NEQ 0 (
    echo Dependency installation failed. Exiting script.
    exit /b 1
)

:: Run userbot
cls
echo Running userbot...
python -m main
if %ERRORLEVEL% NEQ 0 (
    echo Failed to run userbot. Exiting script.
    exit /b 1
)

echo Userbot configured successfully.
endlocal
exit /b 0
