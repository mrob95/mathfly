'''
Created on Sep 4, 2018

@author: Mike Roberts
'''
from mathfly.imports import *

SETTINGS = utilities.load_settings()
CORE = utilities.load_config("core.toml")

_LETTERS, _DIRECTIONS = "letters", "directions"
if SETTINGS["alternative_letters"]:
	_LETTERS += "_alt"
if SETTINGS["alternative_directions"]:
	_DIRECTIONS += "_alt"

def alphabet(big, letter):
	Key(letter.upper() if big else letter).execute()

Breathe.add_commands(
    context=None,
    mapping = {
        "configure " + CORE["pronunciation"]:
            Function(utilities.edit_config, fname="core.toml"),
        "configure scientific notebook":
            Function(utilities.edit_config, fname="ScientificNotebook55.toml"),
        "configure (LyX | licks)":
            Function(utilities.edit_config, fname="lyx.toml"),

        "configure math fly [settings]":
            Function(utilities.load_config, config_name="settings.toml"),

        "reboot dragon": Function(utilities.reboot),

        "math fly help": Function(utilities.help),

        "<noCCR_repeatable_key> [<n>]":
            Key("%(noCCR_repeatable_key)s")*Repeat(extra="n"),
        "<noCCR_non_repeatable_key>":
            Key("%(noCCR_non_repeatable_key)s"),
    },
    extras = [
        Choice("noCCR_repeatable_key", CORE["noCCR_repeatable_keys"]),
        Choice("noCCR_non_repeatable_key", CORE["noCCR_non_repeatable_keys"]),
    ],
    ccr=False
)

Breathe.add_commands(
    context=None,
    mapping = {
    	"[<big>] <letter>":
            Function(alphabet),
    	CORE["numbers_prefix"] + " <numbers>":
            Text("%(numbers)s"),
    	"<punctuation>":
            Key("%(punctuation)s"),

        "(<direction> | <modifier> [<direction>]) [(<n50> | <extreme>)]":
            Function(navigation.text_nav),
    	"<repeatable_key> [<n>]":
            Key("%(repeatable_key)s")*Repeat(extra="n"),
    	"<non_repeatable_key>":
            Key("%(non_repeatable_key)s"),

        CORE["dictation_prefix"] + " <text>":
            Function(lambda text: Text(str(text).lower()).execute()),

        "shift click":
            Key("shift:down") + Mouse("left") + Key("shift:up"),
    },
    extras = [
        IntegerRef("n50", 1, 50, 1),
        IntegerRefMF("numbers", 0,   CORE["numbers_max"]),
        Choice("big",               {CORE["capitals_prefix"]: True}, default=False),
        Choice("extreme",           {CORE["extreme"]: True}, default=False),
    	Choice("letter",             CORE[_LETTERS]),
    	Choice("punctuation",        CORE["punctuation"]),
    	Choice("repeatable_key",     CORE["repeatable_keys"]),
    	Choice("non_repeatable_key", CORE["non_repeatable_keys"]),
    	Choice("direction",          CORE[_DIRECTIONS], default="left"),
    	Choice("modifier",           CORE["modifiers"], default=""),
    ],
)
