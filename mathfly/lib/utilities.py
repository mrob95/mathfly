# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

import io
import toml
import os
import re
import sys, time
import traceback
from __builtin__ import True
from subprocess import Popen

import win32gui
import win32ui

from _winreg import (CloseKey, ConnectRegistry, HKEY_CLASSES_ROOT,
    HKEY_CURRENT_USER, OpenKey, QueryValueEx)

from dragonfly.windows.window import Window
from dragonfly import Choice, Clipboard, Key



BASE_PATH = os.path.realpath(__file__).split("\\lib\\")[0].replace("\\", "/")
if BASE_PATH not in sys.path:
    sys.path.append(BASE_PATH)

# filename_pattern was used to determine when to update the list in the element window,
# checked to see when a new file name had appeared
FILENAME_PATTERN = re.compile(r"[/\\]([\w_ ]+\.[\w]+)")


def load_toml_relative(path):
    path = BASE_PATH + "/" + path
    return load_toml_file(path)

def save_toml_relative(data, path):
    path = BASE_PATH + "/" + path
    return save_toml_file(data, path)

def get_full_path(path):
    return BASE_PATH + "/" + path


def read_selected(same_is_okay=False):
    '''Returns a tuple:
    (0, "text from system") - indicates success
    (1, None) - indicates no change
    (2, None) - indicates clipboard error
    '''
    time.sleep(0.05)
    cb = Clipboard(from_system=True)
    temporary = None
    prior_content = None
    try:
        prior_content = Clipboard.get_system_text()
        Clipboard.set_system_text("")
        Key("c-c").execute()
        time.sleep(0.05)
        temporary = Clipboard.get_system_text()
        cb.copy_to_system()
    except Exception:
        return 2, None
    if prior_content == temporary and not same_is_okay:
        return 1, None
    return 0, temporary

def paste_string(content):
    time.sleep(0.05)
    cb = Clipboard(from_system=True)
    try:
        Clipboard.set_system_text(str(content))
        Key("c-v").execute()
        time.sleep(0.05)
        cb.copy_to_system()
    except Exception:
        return False
    return True

def reboot():
    popen_parameters = []
    popen_parameters.append(BASE_PATH + "/config/bin/reboot.bat")
    popen_parameters.append("C:/Program Files (x86)/Nuance/NaturallySpeaking15/Program/natspeak.exe")

    print(popen_parameters)
    Popen(popen_parameters)

def load_templates(path):
    with open(path, "r+") as f:
        titleq = re.compile(r"^\+\+\+(.*)\+\+\+")
        commentq = re.compile(r"^#.*")
        current = ""
        templates = {}
        for line in f.readlines():
            commentmatch = commentq.search(line)
            titlematch = titleq.search(line)
            if commentmatch:
                pass
            elif titlematch:
                if current and templates[current][-2:] == "\n":
                    templates[current] = templates[current][:-2]
                current = titlematch.group(1)
                templates[current] = ""
            else:
                if current:
                    templates[current] += line
    return templates


def save_toml_file(data, path):
    try:
        formatted_data = unicode(toml.dumps(data))
        with io.open(path, "wt", encoding="utf-8") as f:
            f.write(formatted_data)
    except Exception:
        # simple_log(True)
        pass


def load_toml_file(path):
    result = {}
    try:
        with io.open(path, "rt", encoding="utf-8") as f:
            result = toml.loads(f.read())
    except IOError as e:
        if e.errno == 2:  # The file doesn't exist.
            save_toml_file(result, path)
        else:
            raise
    return result


def list_to_string(l):
    return u"\n".join([unicode(x) for x in l])


def availability_message(feature, dependency):
    print(feature + " feature not available without " + dependency)


def remote_debug(who_called_it=None):
    if who_called_it is None:
        who_called_it = "An unidentified process"
    try:
        import pydevd  # @UnresolvedImport pylint: disable=import-error
        pydevd.settrace()
    except Exception:
        print("ERROR: " + who_called_it +
              " called utilities.remote_debug() but the debug server wasn't running.")


def default_browser_command():
    '''
    Tries to get default browser command, returns either a space delimited
    command string with '%1' as URL placeholder, or empty string.
    '''
    browser_class = 'Software\\Microsoft\\Windows\\Shell\\Associations\\UrlAssociations\\https\\UserChoice'
    try:
        reg = ConnectRegistry(None,HKEY_CURRENT_USER)
        key = OpenKey(reg, browser_class)
        value, t = QueryValueEx(key, 'ProgId')
        CloseKey(key)
        CloseKey(reg)
        reg = ConnectRegistry(None,HKEY_CLASSES_ROOT)
        key = OpenKey(reg, '%s\\shell\\open\\command' % value)
        path, t = QueryValueEx(key, None)
    except WindowsError as e:
        #logger.warn(e)
        return ''
    finally:
        CloseKey(key)
        CloseKey(reg)
    return path
