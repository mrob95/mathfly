from dragonfly import Key, Mouse, AppContext
from dragonfly import Text as TextBase

class Text(TextBase):
    _pause_default = 0.003
    def __init__(self, spec=None, static=False, pause=_pause_default, autofmt=False, use_hardware=False):
        TextBase.__init__(self, spec=spec, static=static, pause=pause, autofmt=autofmt, use_hardware=use_hardware)


from mathfly.lib import utilities
SETTINGS = utilities.load_toml_relative("config/settings.toml")
# Override imported dragonfly actions with aenea's if the 'use_aenea' setting is set to true.
if "use_aenea" in SETTINGS and SETTINGS["use_aenea"]:
    try:
        from aenea import Key, Text, Mouse
        from aenea import ProxyAppContext as AppContext
    except ImportError:
        print("Unable to import aenea actions. Dragonfly actions will be used "
              "instead.")
