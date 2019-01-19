from dragonfly import (Function, Grammar, Text, Dictation, Choice, Pause)

import os, sys
import logging
logging.basicConfig()

from mathfly.lib import control, utilities
from mathfly.lib.dfplus.merge.mergerule import MergeRule
from mathfly.lib.dfplus.merge.mergepair import MergeInf
_NEXUS = control.nexus()

BASE_PATH = os.path.realpath(__file__).split("\\_mathfly_main.py")[0].replace("\\", "/")
sys.path.append(BASE_PATH)

from mathfly.ccr import core, sn_mathematics, lyx_mathematics, latex, alias
_NEXUS.merger.update_config()
_NEXUS.merger.merge(MergeInf.BOOT)
print("*- Starting mathfly -*")
print("modules available:")
for ccr_choice in _NEXUS.merger.global_rule_names():
    print(ccr_choice)


def rebuild():
    _NEXUS.merger.wipe()
    _NEXUS.merger._global_rules = {}
    for module in [core, sn_mathematics, lyx_mathematics, latex]:
        reload(module)
    _NEXUS.merger.update_config()
    _NEXUS.merger.merge(MergeInf.BOOT)
    print("*- Starting mathfly -*")
    print("modules available:")
    for ccr_choice in _NEXUS.merger.global_rule_names():
        print(ccr_choice)


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

        "rebuild math fly": Function(rebuild),
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