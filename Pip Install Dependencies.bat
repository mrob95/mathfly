@echo off
echo Installing: dragonfly2, wxPython, pillow

cd c:\python27\scripts
pip install --upgrade pip
pip install -U wxpython
pip install -U pywin32
pip install -U setuptools
pip install -U future
pip install -U dragonfly2
pip install -U toml
pip install -U beautifulsoup4
pip install -U six

echo ------------------------------------------
echo Mathfly Dependencies Installation Complete
echo ------------------------------------------

pause