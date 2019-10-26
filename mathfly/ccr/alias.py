from mathfly.imports import *

aliases = DictList("aliases", utilities.load_toml_relative("config/aliases.toml"))

def add_alias(spec):
    _, text = utilities.read_selected(True)
    if text and spec:
        aliases[str(spec)] = text
        utilities.save_toml_relative(dict(aliases), "config/aliases.toml")

def delete_aliases():
    aliases.clear()
    utilities.save_toml_relative(dict(aliases), "config/aliases.toml")

def delete_alias(alias):
    for k, v in dict(aliases).items():
        if v == alias:
            del aliases[k]
            utilities.save_toml_relative(dict(aliases), "config/aliases.toml")
            break

Breathe.add_commands(
    None,
    {
        "alias <text>": lambda text: add_alias(text),
        "delete all aliases": delete_aliases,
        "delete alias <alias>": delete_alias,
    },
    [DictListRef("alias", aliases),],
    ccr=False
)

Breathe.add_commands(
    None,
    {
        "<alias>": Text("%(alias)s")
    },
    [
        DictListRef("alias", aliases),
    ]
)