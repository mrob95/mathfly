'''
Created on Sep 4, 2018

@author: Mike Roberts
'''
from dragonfly import Function, Choice, IntegerRef, Dictation, Repeat

from mathfly.lib.actions import Text, Key, Mouse, AppContext
from mathfly.lib import control, utilities, execution
from mathfly.lib.merge.mergerule import MergeRule

BINDINGS = utilities.load_toml_relative("config/ScientificNotebook55.toml")
CORE = utilities.load_toml_relative("config/core.toml")

#---------------------------------------------------------------------------

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
    mcontext = AppContext(executable="scientific notebook")
    pronunciation = BINDINGS["pronunciation"]

    compounds = {
        "[<before>] integral from <sequence1> to <sequence2>":
            [Function(lambda: texchar("int")) + Key("c-l"),
            Key("right, c-h"), Key("right")],

        "[<before>] definite from <sequence1> to <sequence2>":
            [Key("c-6, right, c-l"),
            Key("right, c-h"), Key("right, c-left, left")],

        "[<before>] differential <sequence1> by <sequence2>":
            [Key("c-f, d"), Key("down, d"), Key("right")],

        "[<before>] sum from <sequence1> to <sequence2>":
            [Key("f10, i, down:11, enter/25, a, enter, f10, i, down:11, enter/25, b, enter") + Function(lambda: texchar("sum")) + Key("down"),
            Key("up:2"), Key("right")],

        "[<before>] limit from <sequence1> to <sequence2>":
            [Key("f10, i, down:11, enter/25, b, enter") + Function(lambda: texchar("lim")) + Key("down"),
            Function(lambda: texchar("rightarrow")),
            Key("right")],
    }

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

        "matrix <rows> by <cols>":
            Function(matrix),

        "<numbers> <denominator>":
            Key("c-f") + Text("%(numbers)s") + Key("down") + Text("%(denominator)s") + Key("right"),
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

control.nexus().merger.add_app_rule(sn_mathematics())
