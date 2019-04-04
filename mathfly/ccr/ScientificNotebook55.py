'''
Created on Sep 4, 2018

@author: Mike Roberts
'''
from dragonfly import Function, Choice, Key, Text, Mouse, IntegerRef, Dictation, CompoundRule
from dragonfly import AppContext, Grammar, Repeat

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

#---------------------------------------------------------------------------

class SNIntegralRule(CompoundRule):
    spec = "[<normal>] integral from <sequence1> to <sequence2>"
    def _process_recognition(self, node, extras):
        if "normal" in extras:
            for action in extras["normal"]: action.execute()
        Function(lambda: texchar("int")).execute()
        Key("c-l").execute()
        for action in extras["sequence1"]: action.execute()
        Key("right, c-h").execute()
        for action in extras["sequence2"]: action.execute()
        Key("right").execute()

class SNDiffRule(CompoundRule):
    spec = "[<normal>] differential <sequence1> by <sequence2>"
    def _process_recognition(self, node, extras):
        if "normal" in extras:
            for action in extras["normal"]: action.execute()
        Key("c-f, d").execute()
        for action in extras["sequence1"]: action.execute()
        Key("down, d").execute()
        for action in extras["sequence2"]: action.execute()
        Key("right").execute()

class SNSumRule(CompoundRule):
    spec = "[<normal>] sum from <sequence1> to <sequence2>"
    def _process_recognition(self, node, extras):
        if "normal" in extras:
            for action in extras["normal"]: action.execute()
        Key("f10, i, down:11, enter/25, a, enter, f10, i, down:11, enter/25, b, enter").execute()
        Function(lambda: texchar("sum")).execute()
        Key("down").execute()
        for action in extras["sequence1"]: action.execute()
        Key("up:2").execute()
        for action in extras["sequence2"]: action.execute()
        Key("right").execute()

class SNLimitRule(CompoundRule):
    spec = "[<normal>] limit from <sequence1> to <sequence2>"
    def _process_recognition(self, node, extras):
        if "normal" in extras:
            for action in extras["normal"]: action.execute()
        Key("f10, i, down:11, enter/25, b, enter").execute()
        Function(lambda: texchar("lim")).execute()
        Key("down").execute()
        for action in extras["sequence1"]: action.execute()
        Function(lambda: texchar("rightarrow")).execute()
        for action in extras["sequence2"]: action.execute()
        Key("right").execute()

#---------------------------------------------------------------------------

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
    compounds = [SNIntegralRule, SNDiffRule, SNSumRule, SNLimitRule]
    mwith = CORE["pronunciation"]
    mcontext = AppContext(executable="scientific notebook")
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

control.nexus().merger.add_app_rule(sn_mathematics())
