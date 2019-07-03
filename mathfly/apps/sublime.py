from mathfly.imports import *

class SublimeRule(MergeRule):
    pronunciation = "sublime"
    mcontext = AppContext(executable="sublime_text", title="Sublime Text")

    mapping = {
        "new (file | pane)": Key("c-n"),
        # {"keys": ["ctrl+alt+n"], "command": "new_window"},
        "new window":   Key("ca-n"),
        "open file":    Key("c-o"),
        # {"keys": ["ctrl+shift+o"], "command": "prompt_add_folder"},
        "open folder":  Key("cs-o"),
        "save as":  Key("cs-s"),
        #
        "comment line": Key("c-slash"),
        "comment (block | lines)":    Key("cs-slash"),
        "outdent lines":    Key("c-lbracket"),
        "join lines [<n3>]":    Key("c-j"),
        "match bracket":    Key("c-m"),
        #
        # "(select | sell) all":  Key("c-a"),
        "(select | sell) scope [<n2>]": Key("cs-space"),
        "(select | sell) brackets [<n2>]":  Key("cs-m"),
        "(select | sell) line [<n2>]":  Key("c-l"),
        "(select | sell) indent":   Key("cs-j"),
        # {"keys": ["ctrl+alt+p"], "command": "expand_selection_to_paragraph"},
        "(select | sell) paragraph":    Key("ca-p"),
        # SelectUntil
        "(select | sell) until":    Key("as-s"),

        "toggle side bar": Key("c-k, c-b"),

        #
        "find": Key("c-f"),
        "get all":  Key("a-enter"),
        "replace":  Key("c-h"),
        "edit lines":   Key("cs-l"),
        "edit next [<n3>]": Key("c-d"),
        "edit skip next [<n3>]": Key("c-k, c-d"),
        "edit all": Key("c-d, a-f3"),
        #
        "transform upper":  Key("c-k, c-u"),
        "transform lower":  Key("c-k, c-l"),
        # {"keys": ["ctrl+k", "ctrl+t"], "command": "title_case"},
        "transform title":  Key("c-k, c-t"),
        #
        "line <n11> [<n12>]": Key("c-g") + Text("%(n11)s" + "%(n12)s") + Key("enter"),
        "go to file":   Key("c-p"),
        "go to word":   Key("c-semicolon"),
        "go to symbol": Key("c-r"),
        "go to [symbol in] project": Key("cs-r"),
        "command pallette": Key("cs-p"),
        "(find | search) in (project | folder | directory)": Key("cs-f"),
        #
        "fold": Key("cs-lbracket"),
        "unfold":   Key("cs-rbracket"),
        "unfold all":   Key("c-k, c-j"),
        "fold [level] <n2>":    Key("c-k, c-%(n2)s"),
        #
        "full screen":  Key("f11"),
        "(set | add) bookmark": Key("c-f2"),
        "next bookmark":    Key("f2"),
        "previous bookmark":    Key("s-f2"),
        "clear bookmarks":  Key("cs-f2"),
        #
        "build it": Key("c-b"),
        # "cancel build": Key("c-break")),
        #
        "record macro": Key("c-q"),
        "play [back] macro [<n3>]": Key("cs-q"),
        "(new | create) snippet":   Key("a-n"),
        #
        "close tab":   Key("c-w"),
        "next tab":    Key("c-pgdown"),
        "previous tab":    Key("c-pgup"),
        "<nth> tab":    Key("a-%(n2)s"),
        #
        "column <cols>":    Key("as-%(cols)s"),
        "focus <panel>":    Key("c-%(panel)s"),
        "move <panel>": Key("cs-%(panel)s"),
        # {"keys": ["ctrl+alt+v"], "command": "clone_file"}
        "split right":  Key("as-2, c-1, ca-v, cs-2"),
        #
        "open terminal":    Key("cs-t"),

        "zoom in [<n2>]":   Key("c-equal")*Repeat(extra="n2"),
        "zoom out [<n2>]":   Key("c-minus")*Repeat(extra="n2"),

    }
    extras = [
        IntegerRef("n11", 1, 100),
        IntegerRef("n12", 0, 100),
        IntegerRef("n2", 1, 9),
        IntegerRef("n3", 1, 21),
        Choice("nth", {
            "first": "1",
            "second": "2",
            "third": "3",
            "fourth": "4",
            "fifth": "5",
            "sixth": "6",
            "seventh": "7",
            "eighth": "8",
            "ninth": "9",
            "tenth": "10",
            }),
        Choice("cols", {
            "one": "1",
            "two": "2",
            "three": "3",
            "grid": "5",
        }),
        Choice("panel", {
            "one": "1",
            "left": "1",
            "two": "2",
            "right": "2",
            }),
    ]
    defaults = {
        "n12": "",
        "n2": 1,
        "n3": 1,
    }


#---------------------------------------------------------------------------

control.nexus().merger.add_non_ccr_app_rule(SublimeRule())