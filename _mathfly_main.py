from dragonfly import (Function, Grammar, Text, Dictation, Choice, Pause)

import os, sys
import logging
logging.basicConfig()

from mathfly.lib import control, utilities
from mathfly.lib.merge.mergerule import MergeRule
from mathfly.lib.merge.mergepair import MergeInf
_NEXUS = control.nexus()

BASE_PATH = os.path.realpath(__file__).split("\\_mathfly_main.py")[0].replace("\\", "/")
sys.path.append(BASE_PATH)

from mathfly.ccr import core, sn_mathematics, lyx_mathematics, latex, alias
from mathfly.apps import sublime
_NEXUS.merger.update_config()
_NEXUS.merger.merge(MergeInf.BOOT)
print("*- Starting mathfly -*")
print("Say \"enable <module name>\" to begin, or \"configure <module name>\" to make changes.")
print("Modules available:")
_NEXUS.merger.display_rules()

def rebuild():
    _NEXUS.merger.wipe()
    _NEXUS.merger._global_rules = {}
    for module in [core, sn_mathematics, lyx_mathematics, latex]:
        reload(module)
    _NEXUS.merger.update_config()
    _NEXUS.merger.merge(MergeInf.BOOT)
    print("*- Rebuilt mathfly -*")

def generate_ccr_choices(nexus):
    choices = {}
    for ccr_choice in nexus.merger.global_rule_names():
        choices[ccr_choice] = ccr_choice
    return Choice("name", choices)

def rule_changer(enable, name):
    _NEXUS.merger.global_rule_changer(name=name, enable=enable, save=True)
    if name == "core":
        _NEXUS.merger.selfmod_rule_changer(name2="alias", enable=enable, save=True)

class MainRule(MergeRule):
    
	mapping = {
        "<enable> <name>": Function(rule_changer),

        "reboot dragon": Function(utilities.reboot),

        "rebuild math fly": Function(rebuild),

        "configure <config_name>": Function(utilities.load_config),
	}
	extras=[
		generate_ccr_choices(_NEXUS),
        Choice("config_name", {
            "core": "core",
            "latex": "latex",
            "licks maths": "lyx",
            "scientific notebook maths": "scientific_notebook",
            }),  
        Choice("enable", {
            "enable": True,
            "disable": False
        }),
	]

grammar = Grammar('general')
main_rule = MainRule()
grammar.add_rule(main_rule)
grammar.load()