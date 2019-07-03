from dragonfly import Grammar, Choice
from dragonfly.grammar.recobs import RecognitionHistory

from mathfly.lib import utilities
from mathfly.lib.merge.ccrmerger import CCRMerger
from mathfly.lib.merge.mergepair import MergeInf
import sys
import natlink

class Nexus:
    def __init__(self, real_merger_config=True):
        self.clip = {}
        self.reload_settings()
        self.preserved = None
        self.merger = CCRMerger(real_merger_config)


    def reload_settings(self):
        self.settings = utilities.load_toml_relative("config/settings.toml")

    def delete_words(self, words):
        for word in words:
            try:
                natlink.deleteWord(word)
            except:
                pass

    def add_words(self, words):
        for word in words:
            try:
                natlink.addWord(word)
            except:
                pass

    def load_app_rules(self, apps):
        apploaded = []
        for module_name in apps:
            try:
                lib = __import__("mathfly.apps." + module_name)
                apploaded.append(module_name)
            except Exception as e:
                print("Ignoring rule '{}'. Failed to load with: ".format(module_name))
                print(e)
        if apploaded:
            print("App modules loaded: " + ", ".join(apploaded))

    def load_ccr_rules(self, rules):
        ccrloaded = []
        ccrrebuilt = []
        for module_name in rules:
            if "mathfly.ccr." + module_name in sys.modules:
                try:
                    want_reload_module = sys.modules["mathfly.ccr." + module_name]
                    reload(want_reload_module)
                    ccrrebuilt.append(module_name)
                except Exception as e:
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

    def build(self, startup=False):
        self.reload_settings()
        self.delete_words(self.settings["delete_words"])
        self.add_words(self.settings["add_words"])
        self.merger.wipe()
        self.merger._global_rules = {}
        self.merger._app_rules = {}
        self.merger._self_modifying_rules = {}
        if startup:
            self.load_app_rules(self.settings["app_modules"])
        self.load_ccr_rules(self.settings["ccr_modules"])
        self.merger.update_config()
        self.merger.merge(MergeInf.BOOT)
        if startup:
            print("*- Starting Mathfly -*")
            print("Say \"enable <module name>\" to begin, or \n\"configure <module name>\" to make changes.")
        print("Modules available:")
        self.merger.display_rules()

    def generate_ccr_choices(self, ref):
        return Choice(ref, {rule: rule for rule in self.merger.global_rule_names()})

    def rule_changer(self, enable, name):
        CORE = utilities.load_toml_relative("config/core.toml")

        self.merger.global_rule_changer(name=name, enable=enable, save=True)
        if name == CORE["pronunciation"]:
            self.merger.selfmod_rule_changer(name2="alias", enable=enable, save=True)
