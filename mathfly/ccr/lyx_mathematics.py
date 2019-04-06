'''
Created Jan 2019

@author: Mike Roberts, Alex Boche
'''
from dragonfly import Function, Choice, IntegerRef
from dragonfly import Grammar, Repeat, CompoundRule

from mathfly.lib.actions import Text, Key, Mouse, AppContext
from mathfly.lib import control, utilities, execution
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


class lyx_mathematicsNon(MergeRule):
    mapping = {
        "configure " + BINDINGS["pronunciation"]:
            Function(utilities.load_config, config_name="lyx.toml"),
    }

class lyx_mathematics(MergeRule):
    non = lyx_mathematicsNon
    mwith = CORE["pronunciation"]
    pronunciation = BINDINGS["pronunciation"]

    compounds = {
        "[<before>] integral from <sequence1> to <sequence2>":
            [Text("\\int _"), Key("right, caret"), Key("right")],

        "[<before>] differential <sequence1> by <sequence2>":
            [Key("a-m, f, d"), Key("down, d"), Key("right")],

        "[<before>] sum from <sequence1> to <sequence2>":
            [Text("\\stackrelthree ") + Key("down") + Text("\\sum ") + Key("down"),
            Key("up:2"), Key("right")],

        "[<before>] limit from <sequence1> to <sequence2>":
            [Text("\\underset \\lim ") + Key("down"),
            Text("\\rightarrow "), Key("right")],
    }

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

        "<command>":
            Function(execution.alternating_command),

        "matrix <rows> by <cols>":
            Function(matrix),

        "<numbers> <denominator>":
            Key("a-m, f, %(numbers)s, down, %(denominator)s, right"),

    }

    extras = [
        IntegerRef("rows",    1, BINDINGS["max_matrix_size"]),
        IntegerRef("cols",    1, BINDINGS["max_matrix_size"]),
        IntegerRef("numbers", 0, CORE["numbers_max"]),
        Choice("big",           {CORE["capitals_prefix"]: True}),
        Choice("greek_letter",   BINDINGS["greek_letters"]),
        Choice("symbol1",        BINDINGS["tex_symbols1"]),
        Choice("symbol2",        BINDINGS["tex_symbols2"]),
        Choice("accent",         BINDINGS["accents"]),
        Choice("text_modes",     BINDINGS["text_modes"]),
        Choice("misc_lyx_keys",  BINDINGS["misc_lyx_keys"]),
        Choice("command",        BINDINGS["misc_lyx_commands"]),
        Choice("denominator",    BINDINGS["denominators"]),
    ]

    defaults = {
        "big": False,
    }

# control.nexus().merger.add_global_rule(lyx_mathematics())
context = AppContext(executable="lyx")
control.nexus().merger.add_app_rule(lyx_mathematics(), context)
