'''
Created on Sep 4, 2018

@author: Mike Roberts
'''
from dragonfly import Function, Choice, Key, Text, Mouse, IntegerRef
from dragonfly import AppContext, Grammar, Repeat

from mathfly.lib import control, utilities
from mathfly.lib.merge.mergerule import MergeRule

class SNRule(MergeRule):
    pronunciation = "scientific notebook"

    mapping = {
        "new file": Key("f10, down, enter"),
        "open file": Key("c-o"),
        "save file": Key("f10, down:5, enter"),
        "save as": Key("f10, down:6, enter"),
        "print file": Key("c-p"),
        "export document": Key("f10, down:8, enter"),
        "page preview": Key("f10, down:18, enter"),

        "toggle math": Key("c-m"),
        "toggle text": Key("c-t"),
        "body math": Key("a-2, down, enter"),
        "body text": Key("a-2, down:2, enter"),

        "(begin | insert) [bulleted] list": Key("a-1, down:2, enter"),
        "(begin | insert) numbered list": Key("a-1, down:4, enter"),
        "end [(bulleted | numbered)] list": Key("a-1, up, enter"),

        "insert normal text": Key("a-3, down, enter"),
        "insert (big | large) text": Key("a-3, down:2, enter"),
        "insert small text": Key("a-3, down:9, enter"),
        "insert bold text": Key("a-3, down:3, enter"),
        "insert italic text": Key("a-3, down:6, enter"),
        "insert bold symbols": Key("a-3, down:4, enter"),

        "insert centred text": Key("a-2, down:3, enter"),
        "insert left text": Key("a-2, down:4, enter"),
        "insert right text": Key("a-2, down:5, enter"),
        "insert quotation": Key("a-2, down:11, enter"),
        "insert (heading | title) [one]": Key("a-2, down:6, enter"),
        "insert (heading | title) two": Key("a-2, down:7, enter"),
        "insert (heading | title) three": Key("a-2, down:8, enter"),
        "insert (heading | title) four": Key("a-2, down:9, enter"),
        "insert (heading | title) five": Key("a-2, down:10, enter"),

        "evaluate": Key("c-e"),

        }
    extras = [
        IntegerRef("n", 1, 10),

    ]
    defaults = {
        "n": 1,
    }

context = AppContext(executable="scientific notebook")
grammar = Grammar("scientific notebook", context=context)
rule = SNRule(name="scientific notebook")
grammar.add_rule(rule)
grammar.load()