'''
Created on Sep 4, 2018

@author: Mike Roberts
'''
from dragonfly import Function, Choice, Key, Text, Mouse, IntegerRef

from mathfly.lib import control, utilities
from mathfly.lib.dfplus.merge.mergerule import MergeRule

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
    pronunciation = "core"

    mapping = {
    	"[<big>] <letter>": Function(alphabet),
    	"[numb] <numbers>": Key("%(numbers)s"),
    	"<punctuation>": Key("%(punctuation)s"),

    	"[<modifier>] <direction> [<n>]": Key("%(modifier)s" + "%(direction)s:%(n)s"),
    	"<key> [<n>]": Key("%(key)s:%(n)s"),
    	"<misc_core_keys>": Key("%(misc_core_keys)s"),
        "splat [<n>]": Key("c-backspace:%(n)s")
    	"core test": Text("test successful"),
    	}

    extras = [
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
        CORE["capitals_prefix"]: False,
    	"n": "1",
    	"modifier": "",
    }


control.nexus().merger.add_global_rule(core())