from dragonfly.language.base.integer import Integer
from dragonfly.grammar.elements_basic import RuleWrap
import utilities
import importlib
SETTINGS = utilities.load_settings()

lang = SETTINGS["language"]

try:
  lib = importlib.import_module("mathfly.lib.numbers.%s" % lang)
  IntegerContent = lib.IntegerContent
  print("Numbers from language %s active" % lang)
except ImportError as e:
  from mathfly.lib.numbers.eng import IntegerContent

class IntegerRefMF(RuleWrap):
    def __init__(self, name, min, max, default=None):
        element = Integer(None, min, max, content=IntegerContent)
        RuleWrap.__init__(self, name, element, default=default)
