'''
Created on Sep 4, 2018

@author: Mike Roberts
'''
from mathfly.imports import *

SETTINGS = utilities.load_toml_relative("config/settings.toml")
CORE = utilities.load_toml_relative("config/core.toml")

_LETTERS, _DIRECTIONS = "letters", "directions"
if SETTINGS["alternative_letters"]:
	_LETTERS += "_alt"
if SETTINGS["alternative_directions"]:
	_DIRECTIONS += "_alt"

def alphabet(big, letter):
	if big:
		letter = letter.upper()
	Key(letter).execute()

class coreNon(MergeRule):
    mapping = {
        "configure " + CORE["pronunciation"]:
            Function(utilities.load_config, config_name="core.toml"),
        "configure scientific notebook":
            Function(utilities.load_config, config_name="ScientificNotebook55.toml"),
        "configure (LyX | licks)":
            Function(utilities.load_config, config_name="lyx.toml"),

        "<noCCR_repeatable_key> [<n>]":
            Key("%(noCCR_repeatable_key)s")*Repeat(extra="n"),
        "<noCCR_non_repeatable_key>":
            Key("%(noCCR_non_repeatable_key)s"),
    }
    extras = [
        IntegerRef("n", 1, 10),
        Choice("noCCR_repeatable_key", CORE["noCCR_repeatable_keys"]),
        Choice("noCCR_non_repeatable_key", CORE["noCCR_non_repeatable_keys"]),
    ]
    defaults = {
        "n": 1,
    }

class core(MergeRule):
    non = coreNon

    pronunciation = CORE["pronunciation"]

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
    	}

    extras = [
        Dictation("text"),
    	IntegerRef("n", 1, 10),
        IntegerRef("n50", 1, 50),
        IntegerRefMF("numbers", 0,   CORE["numbers_max"]),
        Choice("big",               {CORE["capitals_prefix"]: True}),
    	Choice("letter",             CORE[_LETTERS]),
    	Choice("punctuation",        CORE["punctuation"]),
    	Choice("repeatable_key",     CORE["repeatable_keys"]),
    	Choice("non_repeatable_key", CORE["non_repeatable_keys"]),
    	Choice("direction",          CORE[_DIRECTIONS]),
    	Choice("modifier",           CORE["modifiers"]),
        Choice("extreme",           {CORE["extreme"]: True}),
    ]

    defaults = {
        "big"      : False,
        "extreme"  : False,
        "n"        : 1,
        "n50"      : 1,
        "direction": "left",
        "modifier" : "",
    }


control.nexus().merger.add_global_rule(core())