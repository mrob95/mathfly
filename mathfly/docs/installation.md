# Installation
## 1. Python
* Download and install [Python v2.7.X  32-bit](https://sourceforge.net/projects/natlink/files/pythonfornatlink/python2.7.14/python2.7.14.exe/download) or higher but not Python 3

Make sure to select `Add python to path`. This can be done manually by searching for "edit environment variables for your account" and adding your Python27 folder to the list of Path values

## 2. NatLink
* Download and install [Natlink](https://sourceforge.net/projects/natlink/files/natlink/natlinktest4.1/). Use natlink-4.1 victor or newer.

## 3. Mathfly
1. Download Caster from [master branch](https://github.com/synkarius/caster/archive/master.zip). 
2. Open up the zip file downloaded
3. Open the file `mathfly-master`. Copy and paste its contents into an empty folder, this can be any folder but it is common to use `user\Documents\NatLink`.
4. Check and install Caster dependencies by clicking on `Pip Install Dependencies.bat` in `\mathfly\config\bin`
    * This can be done manually by pip installing dragonfly2, toml

## 4. Setup and launch
1. Open the start menu and search for "natlink", click the file called "Configure NatLink via GUI" and run it using python 2.7.
2. Ensure that the details of your DNS setup are correct in the "info" tab.
3. In the "configure" tab, under "NatLink" and "UserDirectory" click enable. When you are prompted for a folder, give it the location of your mathfly folder from step three (`user\Documents\NatLink\mathfly-master`).
4. Reboot Dragon. NatLink should load at the same time, with mathfly commands available. To test this:
    * Say "enable core" to enable the core mathfly commands (numbers, phonetic alphabet).
    * Open a fresh notepad window and try a command like "alpha bravo three hundred".