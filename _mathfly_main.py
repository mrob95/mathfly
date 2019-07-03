from dragonfly import (Function, Grammar, Text, Dictation, Choice, Pause)

import os, sys
import logging
import natlink
logging.basicConfig()

from mathfly.lib import control, utilities
from mathfly.lib.merge.mergerule import MergeRule
from mathfly.lib.merge.mergepair import MergeInf

BASE_PATH = os.path.realpath(__file__).split("\\_mathfly_main.py")[0].replace("\\", "/")
sys.path.append(BASE_PATH)

CORE = utilities.load_toml_relative("config/core.toml")

MF_NEXUS = control.nexus()
MF_NEXUS.build(True)

class MainRule(MergeRule):

	mapping = {
        "configure math fly [settings]":
            Function(utilities.load_config, config_name="settings.toml"),

        "<enable> <name>": Function(MF_NEXUS.rule_changer),

        "reboot dragon": Function(utilities.reboot),

        "rebuild math fly": Function(MF_NEXUS.build),

        "math fly help": Function(utilities.help),
	}
	extras=[
		MF_NEXUS.generate_ccr_choices("name"),
        Choice("enable", {
            "enable": True,
            "disable": False
        }),
	]

grammar = Grammar('general')
main_rule = MainRule()
grammar.add_rule(main_rule)
grammar.load()