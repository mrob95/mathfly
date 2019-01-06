'''
Created on Sep 4, 2018

@author: Mike Roberts
'''
from dragonfly import Function, Choice, Key, Text, Mouse, IntegerRef

from lib import control, utilities

from lib.dfplus.merge.mergerule import MergeRule

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

class mathematics(MergeRule):
    pronunciation = "Scientific notebook maths"

    mapping = {
        "<symbol>":
            Function(texchar),
        #
        "[greek] [<big>] <greek_letter>":
            Function(greek),

        "<misc_sn_keys>":
            Key("%(misc_sn_keys)s"),
        "<misc_sn_text>":
            Text("%(misc_sn_text)s"),
            
        #
        "matrix <rows> by <cols>":
            Function(matrix),

        # "limit": Key("l, l, i, m, left, down"),
        

        "mathematics test": Text("test successful"),

    }

   extras = [
        IntegerRef("rows", 1, 6),
        IntegerRef("cols", 1, 6),
        utilities.Choice_from_file("big", ["bindings/core.toml", "capitals"]),
        utilities.Choice_from_file("greek_letter", ["bindings/scientific_notebook.toml", "greek_letters"]),
        utilities.Choice_from_file("symbol", ["bindings/scientific_notebook.toml", "tex_symbols"]),
        utilities.Choice_from_file("misc_sn_keys", ["bindings/scientific_notebook.toml", "misc_sn_keys"]),
        utilities.Choice_from_file("misc_sn_text", ["bindings/scientific_notebook.toml", "misc_sn_text"]),
        
    ]

    defaults = {
        "big": False,
    }

control.nexus().merger.add_global_rule(mathematics())
