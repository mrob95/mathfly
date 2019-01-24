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

CORE = utilities.load_toml_relative("config/core.toml")
SETTINGS = utilities.load_toml_relative("config/settings.toml")
from mathfly.apps import sublime

# Seems ugly but works
def build():
    _NEXUS.merger.wipe()
    _NEXUS.merger._global_rules = {}
    _NEXUS.merger._self_modifying_rules = {}
    for module_name in SETTINGS["ccr_modules"]:
        if "mathfly.ccr." + module_name in sys.modules:
            try:
                want_reload_module = sys.modules["mathfly.ccr." + module_name]
                reload(want_reload_module)
                print(module_name  + " rebuilt")
            except Exception as e:
                print(e)
        else:
            try:
                lib = __import__("mathfly.ccr." + module_name)
                print(module_name  + " loaded")
            except Exception as e:
                print("Ignoring rule '{}'. Failed to load with: ".format(module_name))
                print(e)
    _NEXUS.merger.update_config()
    _NEXUS.merger.merge(MergeInf.BOOT)
    print("*- Starting mathfly -*")
    print("Say \"enable <module name>\" to begin, or \n\"configure <module name>\" to make changes.")
    print("Modules available:")
    _NEXUS.merger.display_rules()

build()

def generate_ccr_choices(nexus):
    choices = {}
    for ccr_choice in nexus.merger.global_rule_names():
        choices[ccr_choice] = ccr_choice
    return Choice("name", choices)

def rule_changer(enable, name):
    _NEXUS.merger.global_rule_changer(name=name, enable=enable, save=True)
    if name == CORE["pronunciation"]:
        _NEXUS.merger.selfmod_rule_changer(name2="alias", enable=enable, save=True)

class MainRule(MergeRule):
    
	mapping = {
        "<enable> <name>": Function(rule_changer),

        "reboot dragon": Function(utilities.reboot),

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