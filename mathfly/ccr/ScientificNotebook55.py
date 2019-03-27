'''
Created on Sep 4, 2018

@author: Mike Roberts
'''
from dragonfly import Function, Choice, Key, Text, Mouse, IntegerRef, Dictation
from dragonfly import AppContext, Grammar, Repeat

from mathfly.lib import control, utilities, execution
from mathfly.lib.merge.mergerule import MergeRule

BINDINGS = utilities.load_toml_relative("config/ScientificNotebook55.toml")
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

class sn_mathematicsNon(MergeRule):
    mapping = {
        "configure " + BINDINGS["pronunciation"]:
            Function(utilities.load_config, config_name="ScientificNotebook55.toml"),

        "text <dict>":
            Key("c-t") + Function(lambda dict: Text(str(dict).capitalize()).execute()),

        "<control>":
            Key("%(control)s"),

    }
    extras = [
        Dictation("dict"),
        IntegerRef("n", 1, 10),
        Choice("control", BINDINGS["control"]),
    ]


class sn_mathematics(MergeRule):
    non = sn_mathematicsNon
    mwith = CORE["pronunciation"]
    pronunciation = BINDINGS["pronunciation"]

    mapping = {
        BINDINGS["symbol_prefix"] + " <symbol>":
            Function(texchar),
        #
        BINDINGS["greek_prefix"] + " [<big>] <greek_letter>":
            Function(greek),
        BINDINGS["accent_prefix"] + " <accent>":
            Key("%(accent)s"),

        BINDINGS["unit_prefix"] + " <units>":
            Function(lambda units: execution.alternating_command(units)),

        "<misc_sn_keys>":
            Key("%(misc_sn_keys)s"),
        "<misc_sn_text>":
            Text("%(misc_sn_text)s"),

        #
        "matrix <rows> by <cols>":
            Function(matrix),

        "<numbers> <denominator>":
            Key("c-f, %(numbers)s, down, %(denominator)s, right"),
    }

    extras = [
        IntegerRef("rows",    1, BINDINGS["max_matrix_size"]),
        IntegerRef("cols",    1, BINDINGS["max_matrix_size"]),
        IntegerRef("numbers", 0, CORE["numbers_max"]),
        Choice("big",           {CORE["capitals_prefix"]: True}),
        Choice("greek_letter",   BINDINGS["greek_letters"]),
        Choice("units",          BINDINGS["units"]),
        Choice("symbol",         BINDINGS["tex_symbols"]),
        Choice("accent",         BINDINGS["accents"]),
        Choice("misc_sn_keys",   BINDINGS["misc_sn_keys"]),
        Choice("misc_sn_text",   BINDINGS["misc_sn_text"]),
        Choice("denominator",    BINDINGS["denominators"]),
    ]

    defaults = {
        "big": False,
    }

# control.nexus().merger.add_global_rule(sn_mathematics())
context = AppContext(executable="scientific notebook")
control.nexus().merger.add_app_rule(sn_mathematics(), context)
