'''
Created Jan 2019

@author: Mike Roberts, Alex Boche
'''
from dragonfly import Function, Choice, IntegerRef, Grammar, Repeat

from mathfly.lib.actions import Text, Key, Mouse, AppContext
from mathfly.lib.merge.mergerule import MergeRule

class LyxRule(MergeRule):
    pronunciation = "lyx"

    mapping = {
        "new file": Key("c-n"),
        "open file": Key("c-o"),
        "save as": Key("cs-s"),

        "math mode": Key("c-m"),
        "display mode": Key("cs-m"),
        "normal mode": Key("a-p, s"),

        "next tab [<n>]": Key("c-pgdown")*Repeat(extra="n"),
        "(prior | previous) tab [<n>]": Key("c-pgup")*Repeat(extra="n"),
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
            "(numbered formula)": "n",
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
            "[bulleted] list": "b",
            "numbered list": "e",
            "description": "d",
            "part": "0",
            "(section | heading)": "2",
            "sub (section | heading)": "3",
            "sub sub (section | heading)": "4",
            "paragraph": "5",
            "sub paragraph": "6",
            "title": "t",
            "author": "s-a",
            "date": "s-d",
            "abstract": "a",
            "address": "a-a",
            "bibliography": "s-b",
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