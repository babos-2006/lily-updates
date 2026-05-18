@echo off

echo Cleaning old builds...

rmdir /s /q build
rmdir /s /q dist

echo Building Lily AI...

python -m PyInstaller ^
--onefile ^
--windowed ^
--collect-all google.generativeai ^
main.py

echo.
echo Build complete!
pause
