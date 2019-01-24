'''
Created Jan 2019

@author: Mike Roberts, Alex Boche
'''
from dragonfly import Function, Choice, Mouse, IntegerRef, Key, Text
from dragonfly import AppContext, Grammar, Repeat

from mathfly.lib import control, utilities
from mathfly.lib.merge.mergerule import MergeRule

BINDINGS = utilities.load_toml_relative("config/lyx.toml")
CORE = utilities.load_toml_relative("config/core.toml")

def greek(big, greek_letter):
    if big:
        greek_letter = greek_letter.title()
    Text("\\" + greek_letter + " ").execute()

def matrix(rows, cols):
    Text("\\" + BINDINGS["matrix_style"] + " ").execute()
    Key("a-m, w, i, "*(rows-1) + "a-m, c, i, "*(cols-1)).execute()

# Alternate between executing as text and executing as keys
def misc(misc_lyx_commands):
    if type(misc_lyx_commands) in [str, int]:
        Text(misc_lyx_commands).execute()
    elif type(misc_lyx_commands) in [list, tuple]:
        for i in range(len(misc_lyx_commands)):
            if i%2==0:
                Text(misc_lyx_commands[i]).execute()
            else:
                Key(misc_lyx_commands[i]).execute()

class lyx_mathematics(MergeRule):
    pronunciation = BINDINGS["pronunciation"]

    mapping = {
        BINDINGS["symbol1_prefix"] + " <symbol1>":
            Text("\\%(symbol1)s "),

        BINDINGS["symbol2_prefix"] + " <symbol2>":
            Text("\\%(symbol2)s "),

        BINDINGS["accent_prefix"] + " <accent>":
            Key("a-m, %(accent)s"),

        BINDINGS["text_prefix"] + " <text_modes>":
            Text("\\%(text_modes)s "),

        BINDINGS["greek_prefix"] + " [<big>] <greek_letter>":
            Function(greek),

        "<misc_lyx_keys>":
            Key("%(misc_lyx_keys)s"),
            
        "<misc_lyx_commands>":
            Function(misc),

        "matrix <rows> by <cols>":
            Function(matrix),

        "<numbers> <denominator>":
            Key("a-m, f, %(numbers)s, down, %(denominator)s, right"),

        "configure " + BINDINGS["pronunciation"]: 
            Function(utilities.load_config, config_name="lyx.toml"),
    }

    extras = [
        IntegerRef("rows", 1, BINDINGS["max_matrix_size"]),
        IntegerRef("cols", 1, BINDINGS["max_matrix_size"]),
        IntegerRef("numbers", 0, CORE["numbers_max"]),
        Choice("big", {CORE["capitals_prefix"]: True}),
        Choice("greek_letter", BINDINGS["greek_letters"]),
        Choice("symbol1", BINDINGS["tex_symbols1"]),
        Choice("symbol2", BINDINGS["tex_symbols2"]),
        Choice("accent", BINDINGS["accents"]),
        Choice("text_modes", BINDINGS["text_modes"]),
        Choice("misc_lyx_keys", BINDINGS["misc_lyx_keys"]),
        Choice("misc_lyx_commands", BINDINGS["misc_lyx_commands"]),
        Choice("denominator", BINDINGS["denominators"]),
    ]

    defaults = {
        "big": False,
    }

control.nexus().merger.add_global_rule(lyx_mathematics())
