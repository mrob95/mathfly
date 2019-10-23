import logging
import natlink
logging.basicConfig()

from mathfly.imports import *

BASE_PATH = os.path.realpath(__file__).split("\\_mathfly_main.py")[0].replace("\\", "/")
sys.path.append(BASE_PATH)

CORE = utilities.load_toml_relative("config/core.toml")
SETTINGS = utilities.load_toml_relative("config/settings.toml")

Breathe.add_global_extras(
    Dictation("text", default=""),
    IntegerRef("n", 1, 20, 1)
)

Breathe.load_modules(
    {
        "mathfly": SETTINGS["modules"]
    }
)

Breathe.add_commands(
    None,
	mapping = {
        "configure math fly [settings]":
            Function(utilities.load_config, config_name="settings.toml"),

        "reboot dragon": Function(utilities.reboot),

        "math fly help": Function(utilities.help),
	},
    ccr=False
)