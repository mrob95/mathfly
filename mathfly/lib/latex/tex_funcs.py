from dragonfly import Function, Key, Text, Clipboard
from mathfly.lib import control, utilities
from mathfly.lib.latex import bibtexer, book_citation_generator
import codecs
import sys

# Return \first{second}, if second is empty then end inside the brackets for user input
def back_curl(first, second):
    if str(second) != "":
        return (Text("\\") + Text(str(first)) + Key("lbrace, rbrace, left") + Text(
            str(second)) + Key("right"))
    if str(second) == "":
        return (Text("\\") + Text(str(first)) + Key("lbrace, rbrace, left"))

def greek_letters(big, greek_letter):
    if big:
        greek_letter = greek_letter.title()
    Text("\\" + str(greek_letter) + " ").execute()

def symbol(symbol):
    if type(symbol) in [str, unicode, int]:
        Text("\\" + symbol + " ").execute()
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
    e, text = utilities.read_selected(False)
    if type(environment) in [str, unicode]:
        env, arg = environment, ""
    elif type(environment) in [tuple, list]:
        env, arg = environment[0], environment[1]
    back_curl("begin", env).execute()
    Text(arg + "\n").execute()
    if text:
        utilities.paste_string(text)
    Key("enter").execute()
    back_curl("end", env).execute()
    if not text:
        Key("up").execute()

def selection_to_bib(ref_type, bib_path):
    Key("c-c/20").execute()
    cb = Clipboard.get_system_text()
    if ref_type == "book":
        ref = book_citation_generator.citation_from_name(cb)
    elif ref_type == "paper":
        ref = bibtexer.bib_from_title(cb)
    elif ref_type == "link":
        ref = bibtexer.bibtex_from_link(cb)
    with codecs.open(bib_path, encoding="utf-8", mode="a") as f:
        f.write(ref)
    print("Reference added:\n" + ref)
    Clipboard.set_system_text(bibtexer.get_tag(ref))
