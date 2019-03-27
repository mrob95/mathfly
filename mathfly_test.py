import os, sys

from mathfly.lib import control, utilities
from mathfly.lib.merge.mergerule import MergeRule
from mathfly.lib.merge.mergepair import MergeInf
_NEXUS = control.nexus()


CORE = utilities.load_toml_relative("config/core.toml")
SETTINGS = utilities.load_toml_relative("config/settings.toml")
_NEXUS.merger.wipe()
_NEXUS.merger._global_rules = {}
_NEXUS.merger._app_rules = {}
_NEXUS.merger._self_modifying_rules = {}
for module_name in SETTINGS["app_modules"]:
    lib = __import__("mathfly.apps." + module_name)
    assert("mathfly.apps." + module_name in sys.modules)
for module_name in SETTINGS["ccr_modules"]:
    lib = __import__("mathfly.ccr." + module_name)
    assert("mathfly.ccr." + module_name in sys.modules)

_NEXUS.merger.update_config()
_NEXUS.merger.merge(MergeInf.BOOT)

