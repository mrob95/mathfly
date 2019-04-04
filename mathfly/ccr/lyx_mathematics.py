'''
Created Jan 2019

@author: Mike Roberts, Alex Boche
'''
from dragonfly import Function, Choice, Mouse, IntegerRef, Key, Text
from dragonfly import AppContext, Grammar, Repeat, CompoundRule

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

#---------------------------------------------------------------------------

class LyXIntegralRule(CompoundRule):
    spec = "[<normal>] integral from <sequence1> to <sequence2>"
    def _process_recognition(self, node, extras):
        if "normal" in extras:
            for action in extras["normal"]: action.execute()
        Text("\\int _").execute()
        for action in extras["sequence1"]: action.execute()
        Key("right, caret").execute()
        for action in extras["sequence2"]: action.execute()
        Key("right").execute()

class LyXDiffRule(CompoundRule):
    spec = "[<normal>] differential <sequence1> by <sequence2>"
    def _process_recognition(self, node, extras):
        if "normal" in extras:
            for action in extras["normal"]: action.execute()
        Key("a-m, f, d").execute()
        for action in extras["sequence1"]: action.execute()
        Key("down, d").execute()
        for action in extras["sequence2"]: action.execute()
        Key("right").execute()

class LyXSumRule(CompoundRule):
    spec = "[<normal>] sum from <sequence1> to <sequence2>"
    def _process_recognition(self, node, extras):
        if "normal" in extras:
            for action in extras["normal"]: action.execute()
        (Text("\\stackrelthree ") + Key("down") + Text("\\sum ") + Key("down")).execute()
        for action in extras["sequence1"]: action.execute()
        Key("up:2").execute()
        for action in extras["sequence2"]: action.execute()
        Key("right").execute()

class LyXLimitRule(CompoundRule):
    spec = "[<normal>] limit from <sequence1> to <sequence2>"
    def _process_recognition(self, node, extras):
        if "normal" in extras:
            for action in extras["normal"]: action.execute()
        Text("\\underset \\lim ").execute()
        Key("down").execute()
        for action in extras["sequence1"]: action.execute()
        Text("\\rightarrow ").execute()
        for action in extras["sequence2"]: action.execute()
        Key("right").execute()

#---------------------------------------------------------------------------

class lyx_mathematicsNon(MergeRule):
    mapping = {
        "configure " + BINDINGS["pronunciation"]:
            Function(utilities.load_config, config_name="lyx.toml"),
    }

class lyx_mathematics(MergeRule):
    non = lyx_mathematicsNon
    compounds = [LyXIntegralRule, LyXDiffRule, LyXSumRule, LyXLimitRule]
    mwith = CORE["pronunciation"]
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
