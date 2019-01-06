'''
Created on Sep 4, 2018

@author: Mike Roberts
'''
from dragonfly import Function, Choice, Key, Text, Mouse, IntegerRef

from lib import control, utilities

from lib.dfplus.merge.mergerule import MergeRule
import os

BASE_PATH = os.path.realpath(__file__).split("\\core.py")[0].replace("\\", "/")

SETTINGS = utilities.load_toml_file(BASE_PATH + "/bindings/settings.toml")

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
    	utilities.Choice_from_file("big", ["bindings/core.toml", "capitals"]),
    	utilities.Choice_from_file("letter", ["bindings/core.toml", _LETTERS]),
    	utilities.Choice_from_file("numbers", ["bindings/core.toml", "numbers"]),
    	utilities.Choice_from_file("punctuation", ["bindings/core.toml", "punctuation"]),
    	utilities.Choice_from_file("key", ["bindings/core.toml", "keys"]),
    	utilities.Choice_from_file("misc_core_keys", ["bindings/core.toml", "misc_core_keys"]),
    	utilities.Choice_from_file("direction", ["bindings/core.toml", _DIRECTIONS]),
    	utilities.Choice_from_file("modifier", ["bindings/core.toml", "modifiers"]),
    ]

    defaults = {
    	"n": "1",
    	"modifier": "",
    	"big": False,
    }


control.nexus().merger.add_global_rule(core())