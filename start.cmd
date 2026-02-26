@echo off

echo.
echo Setting up Python virtual environment
echo.
cd backend
if not exist .venv (
    python -m venv .venv
    if "%errorlevel%" neq "0" (
        echo Failed to create virtual environment
        exit /B %errorlevel%
    )
)
call .venv\Scripts\activate.bat
if "%errorlevel%" neq "0" (
    echo Failed to activate virtual environment
    exit /B %errorlevel%
)

echo.
echo Restoring backend python packages
echo.
python -m pip install --upgrade pip
pip install -r requirements.txt
if "%errorlevel%" neq "0" (
    echo Failed to restore backend python packages
    exit /B %errorlevel%
)

echo.
echo Restoring frontend npm packages
echo.
cd ..\frontend
call npm install
if "%errorlevel%" neq "0" (
    echo Failed to restore frontend npm packages
    exit /B %errorlevel%
)

echo.
echo Building frontend
echo.
call npm run build
if "%errorlevel%" neq "0" (
    echo Failed to build frontend
    exit /B %errorlevel%
)

echo.    
echo Starting combined backend and frontend server    
echo.    
cd ..\backend
start http://localhost:8000
call .venv\Scripts\uvicorn app.main:app --port 8000 --reload
if "%errorlevel%" neq "0" (    
    echo Failed to start server    
    exit /B %errorlevel%    
)
