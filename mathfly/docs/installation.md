# Installation
**Requires [Dragon](https://www.nuance.com/en-gb/dragon/business-solutions/dragon-professional-individual.html), ideally version 12+**

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
1. Open the start menu and search for "natlink", click the file called "Configure NatLink via GUI" and run it using python 2.7 (`C:/python27/python.exe`).
2. Ensure that the details of your DNS setup are correct in the "info" tab.
3. In the "configure" tab, under "NatLink" and "UserDirectory" click enable. When you are prompted for a folder, give it the location of the folder containing `_mathfly_main.py` - your mathfly folder from step three (`user\Documents\NatLink\mathfly-master` or`user\Documents\NatLink\mathfly-master\mathfly-master\`).
4. Reboot Dragon. NatLink should load at the same time, with mathfly commands available. To test this:
    * Say "enable core" to enable the core mathfly commands (numbers, phonetic alphabet).
    * Open a fresh notepad window and try a command like "alpha bravo three hundred".

## 5. Getting started
### Scientific Notebook 5.5
1. Say `enable core` and `enable scientific notebook` to activate all of the commands you will need.
2. Open Scientific notebook. Say `new file` to open a blank document.
3. Say `body math` to get into mathematics dictation mode.
4. To enter the quadratic formula, say the following commands:
    * `x-ray equals`
    * `fraction` - starts a fraction
    * `minus bravo`
    * `plus or minus`
    * `square root`
    * `bravo squared`
    * `minus four alpha charlie`
    * `down` - move into the denominator
    * `numb two alpha` - note that the `numb` prefix is used to avoid confusion with the `down two` command.
    * `right shock` - move out of the fraction and begin a new line
5. Try entering all of the commands in one or two breaths.
6. Keep going! See the [Scientific Notebook 5.5 documentation](Scientific_Notebook.pdf) for a full list of the commands which you can use.

### LyX
1. Say `enable core` and `enable LyX` to activate all of the commands you will need.
2. Open LyX. Say `new file` to open a blank document.
3. Say `math mode` to get into mathematics dictation mode.
4. To enter the quadratic formula, say the following commands:
    * `x-ray equals`
    * `fraction` - starts a fraction
    * `minus bravo`
    * `plus or minus`
    * `square root`
    * `bravo squared`
    * `minus four alpha charlie`
    * `down` - move into the denominator
    * `numb two alpha` - note that the `numb` prefix is used to avoid confusion with the `down two` command.
    * `right two shock` - move out of the fraction and the math box and begin a new line
5. Try entering all of the commands in one or two breaths.
6. Keep going! See the [LyX documentation](LyX.pdf) for a full list of the commands which you can use.
