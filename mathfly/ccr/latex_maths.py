'''
Created on Sep 4, 2018

@author: Mike Roberts
'''
from mathfly.imports import *

BINDINGS = utilities.load_toml_relative("config/latex.toml")
CORE = utilities.load_toml_relative("config/core.toml")

def symbol(symbol):
    if type(symbol) in [str, unicode, int]:
        Text("\\" + symbol + " ").execute()
    else:
        Text("\\" + str(symbol[0])).execute()
        Text("{}"*int(symbol[1])).execute()
        Key("left:" + str(2*int(symbol[1])-1)).execute()

class LaTeXmath(MergeRule):
    pronunciation = BINDINGS["pronunciation"]  +  " maths"

    mapping = {
        "<numbers>": Text("%(numbers)s"),
        "<symbol>":  Function(symbol),
        "<misc_symbol>":
            Alternating("misc_symbol"),
    }

    extras = [
        IntegerRef("numbers", 0, CORE["numbers_max"]),
        Choice("symbol", BINDINGS["symbols"]),
        Choice("misc_symbol", BINDINGS["misc_symbols"]),
        ]
    defaults = {
    }


control.nexus().merger.add_global_rule(LaTeXmath())
