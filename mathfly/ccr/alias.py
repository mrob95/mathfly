from dragonfly import Dictation, Choice, Text, Function, IntegerRef


from mathfly.lib import utilities, control
from mathfly.lib.dfplus.merge.selfmodrule import SelfModifyingRule

_NEXUS = control.nexus()


def delete_all(alias, path):
    aliases = utilities.load_toml_relative("config/aliases.toml")
    aliases[path] = {}
    utilities.save_toml_relative(aliases, "config/aliases.toml")
    alias.refresh()


class Alias(SelfModifyingRule):
    mapping = {"default command": ""}
    toml_path = "single_aliases"
    pronunciation = "alias"
    extras = [
        IntegerRef("n", 1, 50), 
        Dictation("s"),
                ]
    defaults = {
        "n": 1,
        "s": "",
    }

    def alias(self, spec):
        spec = str(spec)
        if spec != "":
            text = utilities.read_selected_without_altering_clipboard()
            if text != None: self.refresh(spec, str(text))

    def refresh(self, *args):
        '''args: spec, text'''
        aliases = utilities.load_toml_relative("config/aliases.toml")
        if not Alias.toml_path in aliases:
            aliases[Alias.toml_path] = {}
        if len(args) > 0:
            aliases[Alias.toml_path][args[0]] = args[1]
            utilities.save_toml_relative(aliases, "config/aliases.toml")
        mapping = {}
        for spec in aliases[Alias.toml_path]:
            mapping[spec] = Function(utilities.paste_string_without_altering_clipboard, 
                    content=str(aliases[Alias.toml_path][spec]))
        mapping["alias <s>"] = Function(lambda s: self.alias(s))
        mapping["delete aliases"] = Function(lambda: delete_all(self, Alias.toml_path)),
        self.reset(mapping)

control.nexus().merger.add_selfmodrule(Alias())
