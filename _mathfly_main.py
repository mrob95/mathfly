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

# Seems ugly but works
def build(startup=False):
    SETTINGS = utilities.load_toml_relative("config/settings.toml")
    if startup:
        apploaded = []
        for module_name in SETTINGS["app_modules"]:
            try:
                lib = __import__("mathfly.apps." + module_name)
                apploaded.append(module_name)
            except Exception as e:
                print("Ignoring rule '{}'. Failed to load with: ".format(module_name))
                print(e)
        if apploaded:
            print("App modules loaded: " + ", ".join(apploaded))
    _NEXUS.merger.wipe()
    _NEXUS.merger._global_rules = {}
    _NEXUS.merger._self_modifying_rules = {}
    ccrloaded = []
    ccrrebuilt = []
    for module_name in SETTINGS["ccr_modules"]:
        if "mathfly.ccr." + module_name in sys.modules:
            try:
                want_reload_module = sys.modules["mathfly.ccr." + module_name]
                reload(want_reload_module)
                ccrrebuilt.append(module_name)
            except Exception as e:
                print("Ignoring rule '{}'. Failed to load with: ".format(module_name))
                print(e)
        else:
            try:
                lib = __import__("mathfly.ccr." + module_name)
                ccrloaded.append(module_name)
            except Exception as e:
                print("Ignoring rule '{}'. Failed to load with: ".format(module_name))
                print(e)
    if ccrloaded:
        print("CCR modules loaded: " + ", ".join(ccrloaded))
    if ccrrebuilt:
        print("CCR modules rebuilt: " + ", ".join(ccrrebuilt))
    _NEXUS.merger.update_config()
    _NEXUS.merger.merge(MergeInf.BOOT)
    print("*- Starting mathfly -*")
    print("Modules available:")
    _NEXUS.merger.display_rules()
    print("Say \"enable <module name>\" to begin, \n\"configure <module name>\" to make changes, \nand \"help mathfly\" to open the documentation")

build(True)

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
        "configure math fly":
            Function(utilities.load_config, config_name="settings.toml"),

        "<enable> <name>": Function(rule_changer),

        "reboot dragon": Function(utilities.reboot),

        "rebuild math fly": Function(build),

        "math fly help": Function(utilities.help),
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