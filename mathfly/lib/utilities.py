# -*- coding: utf-8 -*-
import io, os, sys, time, re
import toml
from subprocess import Popen
from dragonfly import Choice, Clipboard, Key

BASE_PATH = os.path.realpath(__file__).split("\\lib\\")[0].replace("\\", "/")
if BASE_PATH not in sys.path:
    sys.path.append(BASE_PATH)


def save_toml_file(data, path):
    try:
        formatted_data = unicode(toml.dumps(data))
        with io.open(path, "wt", encoding="utf-8") as f:
            f.write(formatted_data)
    except Exception:
        raise

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

def get_full_path(path):
    return BASE_PATH + "/" + path

def load_toml_relative(path):
    path = get_full_path(path)
    return load_toml_file(path)

def save_toml_relative(data, path):
    path = get_full_path(path)
    return save_toml_file(data, path)

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

SETTINGS = load_toml_relative("config/settings.toml")

def reboot():
    Popen([BASE_PATH + "/config/bin/reboot.bat", SETTINGS["dragon_path"]])

def load_config(config_name):
    parameters = []
    parameters.append(SETTINGS["editor_path"])
    parameters.append(get_full_path("config/" + config_name))
    Popen(parameters)
    
def load_text_file(path):
    parameters = []
    parameters.append(SETTINGS["editor_path"])
    parameters.append(path)
    Popen(parameters)
