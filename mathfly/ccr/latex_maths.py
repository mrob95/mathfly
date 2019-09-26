'''
Created on Sep 4, 2018

@author: Mike Roberts
'''
from mathfly.imports import *

BINDINGS = utilities.load_config("latex.toml")
CORE = utilities.load_config("core.toml")

def symbol(symbol):
    if type(symbol) in [str, unicode, int]:
        Text("\\" + symbol + " ").execute()
    else:
        Text("\\" + str(symbol[0])).execute()
        Text("{}"*int(symbol[1])).execute()
        Key("left:" + str(2*int(symbol[1])-1)).execute()

Breathe.add_commands(
    (AppContext(title=BINDINGS["title_contexts"]) | CommandContext(BINDINGS["pronunciation"]))
    & CommandContext(BINDINGS["pronunciation"] + " maths"),
    mapping = {
        "<numbers>": Text("%(numbers)s"),
        "<symbol>":  Function(symbol),
        "<misc_symbol>":
            Alternating("misc_symbol"),
    },
    extras = [
        IntegerRefMF("numbers", 0, CORE["numbers_max"]),
        Choice("symbol", BINDINGS["symbols"]),
        Choice("misc_symbol", BINDINGS["misc_symbols"]),
    ]
)
