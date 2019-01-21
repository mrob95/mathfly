'''
Created Jan 2019

@author: Mike Roberts, Alex Boche
'''
from dragonfly import Function, Choice, Mouse, IntegerRef, Key, Text
from dragonfly import AppContext, Grammar, Repeat

from mathfly.lib import control, utilities
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

# Alternate between executing as text and executing as keys
def misc(misc_lyx_commands):
    if type(misc_lyx_commands) in [str, int]:
        Text(misc_lyx_commands).execute()
    elif type(misc_lyx_commands) in [list, tuple]:
        for i in range(len(misc_lyx_commands)):
            if i%2==0:
                Text(misc_lyx_commands[i]).execute()
            else:
                Key(misc_lyx_commands[i]).execute()

class lyx_mathematics(MergeRule):
    pronunciation = "licks maths"

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
            
        "<misc_lyx_commands>":
            Function(misc),

        "matrix <rows> by <cols>":
            Function(matrix),

        "<numbers> <denominator>":
            Key("a-m, f, %(numbers)s, down, %(denominator)s, right"),
    }

    extras = [
        IntegerRef("rows", 1, BINDINGS["max_matrix_size"]),
        IntegerRef("cols", 1, BINDINGS["max_matrix_size"]),
        IntegerRef("numbers", 0, CORE["numbers_max"]),
        Choice("big", {CORE["capitals_prefix"]: True}),
        Choice("greek_letter", BINDINGS["greek_letters"]),
        Choice("symbol1", BINDINGS["tex_symbols1"]),
        Choice("symbol2", BINDINGS["tex_symbols2"]),
        Choice("accent", BINDINGS["accents"]),
        Choice("text_modes", BINDINGS["text_modes"]),
        Choice("misc_lyx_keys", BINDINGS["misc_lyx_keys"]),
        Choice("misc_lyx_commands", BINDINGS["misc_lyx_commands"]),
        Choice("denominator", BINDINGS["denominators"]),
    ]

    defaults = {
        "big": False,
    }

control.nexus().merger.add_global_rule(lyx_mathematics())


class LyxRule(MergeRule):
    pronunciation = "lyx"

    mapping = {
        "new file": Key("c-n"),
        "open file": Key("c-o"),
        "save as": Key("cs-s"),

        "math mode": Key("c-m"),
        "display mode": Key("cs-m"),

        "undo [<n>]": Key("c-z")*Repeat(extra="n"),
        "redo [<n>]": Key("c-y")*Repeat(extra="n"),
        "next tab [<n>]": Key("c-pgdown")*Repeat(extra="n"),
        "prior tab [<n>]": Key("c-pgup")*Repeat(extra="n"),
        "close tab [<n>]": Key("c-w/20")*Repeat(extra="n"),

        "view PDF": Key("c-r"),
        "update PDF": Key("cs-r"),

        "move line up [<n>]": Key("a-up")*Repeat(extra="n"),
        "move line down [<n>]": Key("a-down")*Repeat(extra="n"),

        "insert <environment>": Key("a-i, h, %(environment)s"),
        "insert <mode>": Key("a-p, %(mode)s"),

        }
    extras = [
        IntegerRef("n", 1, 10),
        Choice("environment", {
            "(in line formula | in line)": "i",
            "(display formula | display)": "d",
            "(equation array environment | equation array)": "e",
            "(AMS align environment | AMS align)": "a",
            "AMS align at [environment]": "t",
            "AMS flalign [environment]": "f",
            "(AMS gathered environment | AMS gather)": "g",
            "(AMS multline [environment]| multiline)": "m",
            "array [environment]": "y",
            "(cases [environment] | piecewise)": "c",
            "(aligned [environment] | align)": "l",
            "aligned at [environment]": "v",
            "gathered [environment]": "h",
            "split [environment]": "s",
            "delimiters": "r",
            "matrix": "x",
            "macro": "o",
            }),  
        Choice("mode", {
            "standard": "s",
            "(itemize | bullets)": "b",
            "(enumerate | numbering)": "e",
            "description": "d",
            
            "part": "0",
            "section": "2",
            "subsection": "3",
            "subsubsection": "4",
            "paragraph": "5",
            "subparagraph": "6",
            "title": "t",
            "author": "s-a",
            "date": "s-d",
            "abstract": "a",
            "address": "a-a",
            "(bibliography | biblio)": "s-b",
            "quotation": "a-q",
            # i'm not sure what the differences between quotation and quote
            "quote": "q",
            "verse": "v",            
        }),
    ]
    defaults = {
        "n": 1,
    }

context = AppContext(executable="lyx")
grammar = Grammar("lyx", context=context)
rule = LyxRule(name="lyx")
grammar.add_rule(rule)
grammar.load()