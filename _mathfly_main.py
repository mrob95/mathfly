import os
os.environ['BREATHE_REBUILD_COMMAND'] = "rebuild mathfly"


import logging
logging.basicConfig()

from mathfly.imports import *

BASE_PATH = os.path.realpath(__file__).split("\\_mathfly_main.py")[0].replace("\\", "/")
sys.path.append(BASE_PATH)

CORE = utilities.load_config("core.toml")
SETTINGS = utilities.load_toml_relative("config/settings.toml")


def delete_words(words):
    for word in words:
        try:
            natlink.deleteWord(word)
        except:
            pass

def add_words(words):
    for word in words:
        try:
            natlink.addWord(word)
        except:
            pass

delete_words(SETTINGS["delete_words"])
add_words(SETTINGS["add_words"])

Breathe.load_modules(
    {
        "mathfly.ccr": "global_extras"
    }
)

Breathe.load_modules(
    {
        "mathfly": SETTINGS["modules"]
    }
)

print("*- Starting Mathfly -*")

del os.environ['BREATHE_REBUILD_COMMAND']