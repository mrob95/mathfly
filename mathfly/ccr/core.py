'''
Created on Sep 4, 2018

@author: Mike Roberts
'''
from dragonfly import Function, Choice, Key, Text, Mouse, IntegerRef, Dictation, Repeat

from mathfly.lib import control, utilities
from mathfly.lib.merge.mergerule import MergeRule

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

class core(MergeRule):
    pronunciation = CORE["pronunciation"]

    mapping = {
    	"[<big>] <letter>": Function(alphabet),
    	CORE["numbers_prefix"] + " <numbers>": Text("%(numbers)s"),
    	"<punctuation>": Key("%(punctuation)s"),

    	"[<modifier>] <direction> [<n>]": Key("%(modifier)s" + "%(direction)s:%(n)s"),
    	"<key> [<n>]": Key("%(key)s")*Repeat(extra="n"),
    	"<misc_core_keys>": Key("%(misc_core_keys)s"),

        CORE["dictation_prefix"] + " <text>": Text("%(text)s"),

        "shift click": Key("shift:down") + Mouse("left") + Key("shift:up"),

        "configure " + CORE["pronunciation"]: Function(utilities.load_config, config_name="core.toml"),

    	}

    extras = [
        Dictation("text"),
    	IntegerRef("n", 1, 10),
        IntegerRef("numbers", 0, CORE["numbers_max"]),
        Choice("big", {CORE["capitals_prefix"]: True}),
    	Choice("letter", CORE[_LETTERS]),
    	Choice("punctuation", CORE["punctuation"]),
    	Choice("key", CORE["keys"]),
    	Choice("misc_core_keys", CORE["misc_core_keys"]),
    	Choice("direction", CORE[_DIRECTIONS]),
    	Choice("modifier", CORE["modifiers"]),
    ]

    defaults = {
        "big": False,
    	"n": 1,
    	"modifier": "",
    }


control.nexus().merger.add_global_rule(core())