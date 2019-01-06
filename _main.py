from dragonfly import (Function, Grammar, Text, Dictation, Choice, Pause)

from lib import control
_NEXUS = control.nexus()

import mathematics
import core
from lib.dfplus.merge.mergerule import MergeRule


def generate_ccr_choices(nexus):
    choices = {}
    for ccr_choice in nexus.merger.global_rule_names():
        choices[ccr_choice] = ccr_choice
    return Choice("name", choices)

class MainRule(MergeRule):
    
	mapping = {
	    "<enable> <name>":
	    	Function(_NEXUS.merger.global_rule_changer(), save=True),

        "hello world": Text("hello <?> world"),
	}
	extras=[
		generate_ccr_choices(_NEXUS),
        Choice("enable", {
            "enable": True,
            "disable": False
        }),
	]

grammar = Grammar('general')
main_rule = MainRule()
grammar.add_rule(main_rule)

grammar.load()

print("*- Starting mathfly -*")
print("modules available:")
for ccr_choice in _NEXUS.merger.global_rule_names():
    print(ccr_choice)

_NEXUS.merger.update_config()
_NEXUS.merger.merge(3)
