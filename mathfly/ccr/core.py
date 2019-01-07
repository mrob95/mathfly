'''
Created on Sep 4, 2018

@author: Mike Roberts
'''
from dragonfly import Function, Choice, Key, Text, Mouse, IntegerRef

from mathfly.lib import control, utilities

from mathfly.lib.dfplus.merge.mergerule import MergeRule
import os

BASE_PATH = os.path.realpath(__file__).split("\\ccr\\")[0].replace("\\", "/")

SETTINGS = utilities.load_toml_file(BASE_PATH + "/config/settings.toml")

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
    pronunciation = "core"

    mapping = {
    	"[<big>] <letter>": Function(alphabet),
    	"<numbers>": Key("%(numbers)s"),
    	"<punctuation>": Key("%(punctuation)s"),

    	"[<modifier>] <direction> [<n>]": Key("%(modifier)s" + "%(direction)s:%(n)s"),
    	"<key> [<n>]": Key("%(key)s:%(n)s"),
    	"<misc_core_keys>": Key("%(misc_core_keys)s"),

    	"core test": Text("test successful"),
    	}

    extras = [
    	IntegerRef("n", 1, 10),
    	utilities.Choice_from_file("big", ["config/core.toml", "capitals"]),
    	utilities.Choice_from_file("letter", ["config/core.toml", _LETTERS]),
    	utilities.Choice_from_file("numbers", ["config/core.toml", "numbers"]),
    	utilities.Choice_from_file("punctuation", ["config/core.toml", "punctuation"]),
    	utilities.Choice_from_file("key", ["config/core.toml", "keys"]),
    	utilities.Choice_from_file("misc_core_keys", ["config/core.toml", "misc_core_keys"]),
    	utilities.Choice_from_file("direction", ["config/core.toml", _DIRECTIONS]),
    	utilities.Choice_from_file("modifier", ["config/core.toml", "modifiers"]),
    ]

    defaults = {
    	"n": "1",
    	"modifier": "",
    	"big": False,
    }


control.nexus().merger.add_global_rule(core())