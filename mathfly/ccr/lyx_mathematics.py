'''
Created on Sep 4, 2018

@author: Mike Roberts
'''
from dragonfly import Function, Choice, Key, Text, Mouse, IntegerRef

from mathfly.lib import control, utilities
from mathfly.lib.dfplus.merge.mergerule import MergeRule

BINDINGS = utilities.load_toml_relative("config/lyx.toml")


def greek(big, greek_letter):
    if big:
        greek_letter = greek_letter.title()
    Text("\\" + greek_letter + " ").execute()

def matrix(rows, cols):
    Text("\\bmatrix ").execute()
    for _ in range(0, rows-1):
        Key("a-m, w, i").execute()
    for _ in range(0, cols-1):
        Key("a-m, c, i").execute()

class lyx_mathematics(MergeRule):
    pronunciation = "licks maths"

    mapping = {
        BINDINGS["symbol1_prefix"] + " <symbol1>":
            Text("\\%(symbol1)s "),
        BINDINGS["symbol2_prefix"] + " <symbol2>":
            Text("\\%(symbol2)s "),

        #
        BINDINGS["greek_prefix"] + " [<big>] <greek_letter>":
            Function(greek),

        "<misc_lyx_keys>":
            Key("%(misc_lyx_keys)s"),
        "<misc_lyx_text>":
            Text("%(misc_lyx_text)s"),
            
        # #
        "matrix <rows> by <cols>":
            Function(matrix),

    }

    extras = [
        IntegerRef("rows", 1, 10),
        IntegerRef("cols", 1, 10),
        utilities.Choice_from_file("big", ["config/core.toml", "capitals"]),
        utilities.Choice_from_file("greek_letter", ["config/lyx.toml", "greek_letters"]),
        utilities.Choice_from_file("symbol1", ["config/lyx.toml", "tex_symbols1"]),
        utilities.Choice_from_file("symbol2", ["config/lyx.toml", "tex_symbols2"]),
        utilities.Choice_from_file("misc_lyx_keys", ["config/lyx.toml", "misc_lyx_keys"]),
        utilities.Choice_from_file("misc_lyx_text", ["config/lyx.toml", "misc_lyx_text"]),
        
    ]

    defaults = {
        "big": False,
    }

control.nexus().merger.add_global_rule(lyx_mathematics())
