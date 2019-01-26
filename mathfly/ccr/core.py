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

class coreNon(MergeRule):
    mapping = {
        "configure " + CORE["pronunciation"]: Function(utilities.load_config, config_name="core.toml"),

        "<noCCR_repeatable_key> [<n>]": Key("%(noCCR_repeatable_key)s")*Repeat(extra="n"),
        "<noCCR_non_repeatable_key>": Key("%(noCCR_non_repeatable_key)s"),
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
    	"[<big>] <letter>": Function(alphabet),
    	CORE["numbers_prefix"] + " <numbers>": Text("%(numbers)s"),
    	"<punctuation>": Key("%(punctuation)s"),

    	"[<modifier>] <direction> [<n>]": Key("%(modifier)s" + "%(direction)s:%(n)s"),
    	"<repeatable_key> [<n>]": Key("%(repeatable_key)s")*Repeat(extra="n"),
    	"<non_repeatable_key>": Key("%(non_repeatable_key)s"),

        CORE["dictation_prefix"] + " <text>": Text("%(text)s"),

        "shift click": Key("shift:down") + Mouse("left") + Key("shift:up"),
    	}

    extras = [
        Dictation("text"),
    	IntegerRef("n", 1, 10),
        IntegerRef("numbers", 0, CORE["numbers_max"]),
        Choice("big", {CORE["capitals_prefix"]: True}),
    	Choice("letter", CORE[_LETTERS]),
    	Choice("punctuation", CORE["punctuation"]),
    	Choice("repeatable_key", CORE["repeatable_keys"]),
    	Choice("non_repeatable_key", CORE["non_repeatable_keys"]),
    	Choice("direction", CORE[_DIRECTIONS]),
    	Choice("modifier", CORE["modifiers"]),
    ]

    defaults = {
        "big": False,
    	"n": 1,
    	"modifier": "",
    }


control.nexus().merger.add_global_rule(core())