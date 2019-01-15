from dragonfly import (Function, Grammar, Text, Dictation, Choice, Pause)

import os, sys
from mathfly.lib import control, utilities
from mathfly.lib.dfplus.merge.mergerule import MergeRule
from mathfly.lib.dfplus.merge.mergepair import MergeInf
_NEXUS = control.nexus()

BASE_PATH = os.path.realpath(__file__).split("\\_mathfly_main.py")[0].replace("\\", "/")
if BASE_PATH not in sys.path:
    sys.path.append(BASE_PATH)

def build():
    _NEXUS.merger._global_rules = {}
    for module in ("core", "sn_mathematics", "lyx_mathematics", "latex"):
        if module in sys.modules.keys():
            del sys.modules[module]
    from mathfly.ccr import core, sn_mathematics, lyx_mathematics, latex
    _NEXUS.merger.merge(MergeInf.BOOT)
    print("*- Starting mathfly -*")
    print("modules available:")
    for ccr_choice in _NEXUS.merger.global_rule_names():
        print(ccr_choice)

build()
_NEXUS.merger.update_config()

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

        "rebuild math fly": Function(build),
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


