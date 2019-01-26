'''
Created on Sep 4, 2018

@author: Mike Roberts
'''
from dragonfly import Function, Choice, Key, Text, Mouse, Repeat, Clipboard

from mathfly.lib import control, utilities, execution
from mathfly.lib.merge.mergerule import MergeRule
from mathfly.lib.bibtex import bibtexer, book_citation_generator

BINDINGS = utilities.load_toml_relative("config/latex.toml")
CORE = utilities.load_toml_relative("config/core.toml")

# Return \first{second}, if second is empty then end inside the brackets for user input
def back_curl(first, second):
    if str(second) != "":
        return (Text("\\") + Text(str(first)) + Key("lbrace, rbrace, left") + Text(
            str(second)) + Key("right"))
    if str(second) == "":
        return (Text("\\") + Text(str(first)) + Key("lbrace, rbrace, left"))

def greek_letters(big, greek_letter):
    if big == "big":
        greek_letter = greek_letter.title()
    Text("\\" + str(greek_letter) + " ").execute()

def symbol(symbol):
    if type(symbol) in [str, unicode, int]:
        Text("\\" + symbol).execute()
    else:
        Text("\\" + str(symbol[0])).execute()
        Text("{}"*int(symbol[1])).execute()
        Key("left:" + str(2*int(symbol[1])-1)).execute()

def quote():
    e, text = utilities.read_selected(False)
    if text:
        Text("``" + text + "\'\'").execute()
    else:
        Text("``\'\'").execute()
        Key("left:2").execute()

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

def selection_to_bib(ref_type):
    Key("c-c/20").execute()
    cb = Clipboard.get_system_text()
    if ref_type == "book":
        ref = book_citation_generator.citation_from_name(cb)
    elif ref_type == "paper":
        ref = bibtexer.bib_from_title(cb)
    elif ref_type == "link":
        ref = bibtexer.bibtex_from_link(cb)
    with open(BINDINGS["bibliography_path"], "a") as f:
        f.write(ref)
        print("Reference added:\n" + ref)
        Clipboard.set_system_text(bibtexer.get_tag(ref))

class LaTeXNon(MergeRule):
    mapping = {
        "configure " + BINDINGS["pronunciation"]: 
            Function(utilities.load_config, config_name="latex.toml"),

        "add <ref_type> to bibliography": Function(selection_to_bib),

        "(open | edit) bibliography": 
            Function(utilities.load_text_file, path=BINDINGS["bibliography_path"]),
    }
    extras = [
        Choice("ref_type", {
                "book": "book",
                "link": "link",
                "paper": "paper",
                }),
    ]

class LaTeX(MergeRule):
    non = LaTeXNon

    pronunciation = BINDINGS["pronunciation"]

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

        BINDINGS["command_prefix"] + " my (bib resource | bibliography)":  back_curl("addbibresource", BINDINGS["bibliography_path"]),

        BINDINGS["command_prefix"] + " quote":  Function(quote),
        #
        "superscript":  Text("^") + Key("lbrace, rbrace, left"),
        "subscript":  Text("_") + Key("lbrace, rbrace, left"),

        BINDINGS["template_prefix"] + " <template>": Function(execution.template),
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
        Choice("template", BINDINGS["templates"]),
        ]
    defaults = {
        "big": False,
        "packopts": "",
        "class": "",
    }


control.nexus().merger.add_global_rule(LaTeX())
