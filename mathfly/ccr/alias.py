from mathfly.imports import *

MF_NEXUS = control.nexus()

class Alias(SelfModifyingRule):
    mapping = {"default command": ""}
    key = "aliases"
    pronunciation = "alias"

    def delete_all(self, key):
        utilities.save_toml_relative({}, "config/aliases.toml")
        self.refresh()

    def alias(self, spec):
        spec = str(spec)
        e, text = utilities.read_selected(True)
        if spec and text:
            self.refresh(spec, str(text))

    def refresh(self, *args):
        '''args: spec, text'''
        aliases = utilities.load_toml_relative("config/aliases.toml")
        if not Alias.key in aliases:
            aliases[Alias.key] = {}
        if len(args) > 0:
            aliases[Alias.key][args[0]] = args[1]
            utilities.save_toml_relative(aliases, "config/aliases.toml")
        mapping = {}
        for spec in aliases[Alias.key]:
            mapping[spec] = Function(utilities.paste_string,
                    content=str(aliases[Alias.key][spec]))
        mapping["alias <s>"] = Function(lambda s: self.alias(s))
        mapping["delete aliases"] = Function(self.delete_all, key=Alias.key)
        self.reset(mapping)

control.nexus().merger.add_selfmodrule(Alias())
