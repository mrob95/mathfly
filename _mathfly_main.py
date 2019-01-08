from dragonfly import (Function, Grammar, Text, Dictation, Choice, Pause)

import os, sys
from mathfly.lib import control, utilities
from mathfly.lib.dfplus.merge.mergerule import MergeRule
_NEXUS = control.nexus()

BASE_PATH = os.path.realpath(__file__).split("\\_mathfly_main.py")[0].replace("\\", "/")
if BASE_PATH not in sys.path:
    sys.path.append(BASE_PATH)

from mathfly.ccr import core, sn_mathematics, lyx_mathematics

def generate_ccr_choices(nexus):
    choices = {}
    for ccr_choice in nexus.merger.global_rule_names():
        choices[ccr_choice] = ccr_choice
    return Choice("name", choices)

class MainRule(MergeRule):
    
	mapping = {
	    "<enable> <name>":
	    	Function(_NEXUS.merger.global_rule_changer(), save=True),

        "reboot dragon":Function(utilities.reboot),
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
