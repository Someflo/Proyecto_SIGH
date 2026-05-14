@echo off
echo ==============================================
echo   Iniciando Servidor SIGH (Modo Portatil USB)
echo ==============================================
echo.

:: Buscar automaticamente la carpeta de WinPython
for /d %%i in (WPy64*) do set WINPYTHON_DIR=%%i

if "%WINPYTHON_DIR%"=="" (
    echo [ERROR] No se encontro la carpeta de WinPython en esta ubicacion.
    echo Por favor, lee el archivo INSTRUCCIONES_USB.txt
    pause
    exit /b
)

:: Encontrar el ejecutable de Python dentro de WinPython
for /d %%p in (%WINPYTHON_DIR%\python-*) do set PYTHON_EXE=%%p\python.exe

if not exist "%PYTHON_EXE%" (
    echo [ERROR] No se pudo encontrar python.exe dentro de %WINPYTHON_DIR%
    pause
    exit /b
)

echo Usando Python desde: %PYTHON_EXE%
echo Iniciando Django...
echo.

"%PYTHON_EXE%" .\Proyecto_SIGH\manage.py runserver

pause
