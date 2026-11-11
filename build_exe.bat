@echo off
color 0a
echo ===================================================
echo   Full Project to Single EXE Builder (PyInstaller)
echo ===================================================
echo.

python -m pip install --upgrade pyinstaller >nul 2>&1

echo Building the entire project into a single EXE file...
echo Please wait, this may take a few seconds...
echo.

:: Packaging all folders and starting from start.py
pyinstaller --noconsole --onefile --add-data "src;src" start.py

echo.
echo ===================================================
echo  Done! Your standalone EXE is ready in the 'dist' folder.
echo ===================================================
pause
