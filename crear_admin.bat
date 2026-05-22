@echo off
cd /d "%~dp0"

echo ==============================================
echo   Crear Administrador SIGH
echo ==============================================
echo.

:: Buscar automaticamente la carpeta de WinPython
for /d %%i in (WPy64*) do set WINPYTHON_DIR=%%i

if "%WINPYTHON_DIR%"=="" (
    echo [ERROR] No se encontro la carpeta de WinPython.
    pause
    exit /b
)

:: Encontrar el ejecutable de Python
for /d %%p in (%WINPYTHON_DIR%\python-*) do set PYTHON_EXE=%%p\python.exe

if not exist "%PYTHON_EXE%" (
    echo [ERROR] No se pudo encontrar python.exe
    pause
    exit /b
)

echo Por favor, inventa un usuario y una contrasena para el administrador.
echo Nota: Cuando escribas la contrasena NO se veran las letras en la pantalla, es normal.
echo.

"%PYTHON_EXE%" .\Proyecto_SIGH\manage.py createsuperuser

echo.
pause
