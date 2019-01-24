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
        "new file": Key("c-n"),
        "open file": Key("c-o"),
        "save as": Key("cs-s"),

        "toggle math": Key("c-m"),
        "toggle text": Key("c-t"),

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