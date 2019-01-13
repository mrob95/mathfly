'''
Created on Sep 4, 2018

@author: Mike Roberts
'''
from dragonfly import Function, Choice, Key, Text, Mouse, IntegerRef

from mathfly.lib import control, utilities
from mathfly.lib.dfplus.merge.mergerule import MergeRule

BINDINGS = utilities.load_toml_relative("config/scientific_notebook.toml")
CORE = utilities.load_toml_relative("config/core.toml")

def texchar(symbol):
    keychain = "ctrl:down, "
    for character in symbol:
        keychain = keychain + character + ", "
    keychain=keychain + "ctrl:up"
    Key(keychain).execute()

def greek(big, greek_letter):
    if big:
        greek_letter = greek_letter.upper()
    Key("c-g, " + greek_letter).execute()

def matrix(rows, cols):
    Key("f10/5, i/5, down:8, enter/50").execute()
    Key(str(rows) + "/50, tab, " + str(cols) + "/50, enter").execute()

class sn_mathematics(MergeRule):
    pronunciation = "Scientific notebook maths"

    mapping = {
        BINDINGS["symbol_prefix"] + " <symbol>":
            Function(texchar),
        #
        BINDINGS["greek_prefix"] + " [<big>] <greek_letter>":
            Function(greek),

        "<misc_sn_keys>":
            Key("%(misc_sn_keys)s"),
        "<misc_sn_text>":
            Text("%(misc_sn_text)s"),
            
        #
        "matrix <rows> by <cols>":
            Function(matrix),

        "mathematics test": Text("test successful"),

    }

    extras = [
        IntegerRef("rows", 1, 6),
        IntegerRef("cols", 1, 6),
        Choice("big", {CORE["capitals_prefix"]: True}),
        Choice("greek_letter", BINDINGS["greek_letters"]),
        Choice("symbol", BINDINGS["tex_symbols"]),
        Choice("misc_sn_keys", BINDINGS["misc_sn_keys"]),
        Choice("misc_sn_text", BINDINGS["misc_sn_text"]),
    ]

    defaults = {
        CORE["capitals_prefix"]: False,
    }

control.nexus().merger.add_global_rule(sn_mathematics())
