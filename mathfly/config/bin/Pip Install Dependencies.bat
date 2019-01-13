@echo off
echo Installing: dragonfly2, wxPython, pillow

cd c:\python27\scripts
pip install setuptools
pip install future
pip install dragonfly2
pip install toml

echo ------------------------------------------
echo Mathfly Dependencies Installation Complete
echo ------------------------------------------

pause