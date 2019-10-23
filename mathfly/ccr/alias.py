from mathfly.imports import *

# aliases = utilities.load_toml_relative("config/aliases.toml")

aliases = DictList("aliases")

def add_alias(spec):
    _, text = utilities.read_selected(True)
    if text and spec:
        aliases[spec] = text

Breathe.add_commands(
    None,
    {
        "alias <text>": lambda text: add_alias(text),
        "delete aliases": lambda: aliases.clear()
    },
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
