'''
Created on Sep 4, 2018

@author: Mike Roberts
'''
from dragonfly import Function, Choice, Key, Text, Mouse, Repeat
import re

from mathfly.lib import control, utilities
from mathfly.lib.dfplus.merge.mergerule import MergeRule

BINDINGS = utilities.load_toml_relative("config/latex.toml")
CORE = utilities.load_toml_relative("config/core.toml")

with open(utilities.get_full_path("config/latex_templates.txt"), "r+") as f:
    query = re.compile(r"^\+\+\+(.*)\+\+\+")
    current = ""
    templates = {}
    for line in f.readlines():
        match = query.search(line)
        if match:
            current = match.group(1)
            templates[current] = ""
        else:
            if current:
                templates[current] += line


# Return \first{second}, if second is empty then end inside the brackets for user input
def back_curl(first, second):
    if str(second) != "":
        return (Text("\\") + Text(str(first)) + Key("lbrace, rbrace, left") + Text(
            str(second)) + Key("right"))
    if str(second) == "":
        return (Text("\\") + Text(str(first)) + Key("lbrace, rbrace, left"))

def greek_letters(big, greek_letter):
    if big == "big":
        symbol = symbol.title()
    Text("\\" + str(symbol) + " ").execute()

def symbol(symbol):
    if type(symbol) in [str, unicode, int]:
        Text("\\" + symbol).execute()
    else:
        Text("\\" + str(symbol[0])).execute()
        for _ in range(int(symbol[1])):
            Text("{}").execute()
        Key("left:" + str(2*int(symbol[1])-1)).execute()

def packages(packopts):
    if type(packopts) in [str, unicode]:
        back_curl("usepackage", packopts).execute()
    elif type(packopts) in [tuple, list]:
        back_curl("usepackage" + packopts[0], packopts[1]).execute()

def begin_end(environment):
    if type(environment) in [str, unicode]:
        env, arg = environment, ""
    elif type(environment) in [tuple, list]:
        env, arg = environment[0], environment[1]
    back_curl("begin", env).execute()
    Text(arg + "\n\n").execute()
    back_curl("end", env).execute()
    Key("up").execute()

class LaTeX(MergeRule):
    pronunciation = "latex"

    mapping = {
        "insert comment":  Text("% "),

        BINDINGS["class_prefix"] + " [<class>]":  back_curl("documentclass", "%(class)s"),

        BINDINGS["environment_prefix"] + " <environment>":  Function(begin_end),
        #
        BINDINGS["package_prefix"] + " [<packopts>]":  Function(packages),
        #
        BINDINGS["symbol_prefix"] + " <symbol>":  Function(symbol),
        BINDINGS["symbol_prefix"] + " degrees": Text("^{\\circ}"),
        BINDINGS["greek_prefix"] + " [<big>] <greek_letter>":  Function(greek_letters),
        #
        BINDINGS["command_prefix"] + " <command>":  back_curl("%(command)s", ""),
        BINDINGS["command_prefix"] + " <commandnoarg>":  Text("\\%(commandnoarg)s "),

        BINDINGS["command_prefix"] + " my bib resource":  back_curl("addbibresource", BINDINGS["bibliography_path"]),

        BINDINGS["command_prefix"] + " quote":  Text("``\'\'") + Key("left:2"),
        #
        "superscript":  Text("^") + Key("lbrace, rbrace, left"),
        "subscript":  Text("_") + Key("lbrace, rbrace, left"),

        BINDINGS["command_prefix"] + " <template>": Text("%(template)s"),

    }

    extras = [
        Choice("big", {CORE["capitals_prefix"]: True}),
        Choice("packopts", BINDINGS["packages"]),
        Choice("class", BINDINGS["document_classes"]),
        Choice("greek_letter", BINDINGS["greek_letters"]),
        Choice("symbol", BINDINGS["symbols"]),
        Choice("commandnoarg", BINDINGS["commandnoarg"]),
        Choice("command", BINDINGS["command"]),
        Choice("environment", BINDINGS["environments"]),
        Choice("template", templates),
        ]
    defaults = {
        CORE["capitals_prefix"]: False,
        "packopts": "",
        "class": "",
    }


control.nexus().merger.add_global_rule(LaTeX())
