'''
Created on Sep 4, 2018

@author: Mike Roberts
'''
from mathfly.imports import *

BINDINGS = utilities.load_config("ScientificNotebook55.toml")
CORE = utilities.load_config("core.toml")

#------------------------------------------------

def TeX(symbol):
    return Key("ctrl:down") + Text(symbol) + Key("ctrl:up")


def greek(big, greek_letter):
    if big:
        greek_letter = greek_letter.upper()
    Key("c-g, " + greek_letter).execute()


def matrix(rows, cols):
    Key("f10/5, i/5, down:8, enter/50").execute()
    Key(str(rows) + "/50, tab, " + str(cols) + "/50, enter").execute()


#------------------------------------------------


<<<<<<< HEAD
Breathe.add_commands(
    AppContext(executable="scientific notebook"),
    {
        "text <text>": Key("c-t")
        + Function(lambda text: Text(text.capitalize()).execute()),
        "<control>": Key("%(control)s"),
    },
    [
=======
        "[<before>] <minmax> by <sequence1>":
            [Key("f10, i, down:11, enter/25, b, enter") + Text("%(minmax)s") + Key("down"),
            Key("right"), None],

        "[<before>] <script1> <singleton1> [<after>]":
            [Key("%(script1)s"), Key("right"), None],

        "[<before>] <script1> <singleton1> <script2> <singleton2> [<after>]":
            [Key("%(script1)s"), Key("right, %(script2)s"), Key("right")],

    }
    extras = [
        Choice("minmax", {
            "(minimum | minimises)": "min",
            "(maximum | maximises)": "max",
            }),
        Choice("script1", {
            "sub": "c-l",
            "super": "c-h",
            }),
        Choice("script2", {
            "sub": "c-l",
            "super": "c-h",
            }),
    ]

class sn_mathematicsNon(MergeRule):
    mapping = {
        "text <dict>":
            Key("c-t") + Function(lambda dict: Text(str(dict).capitalize()).execute()),
        "<control>":
            Key("%(control)s"),
    }
    extras = [
        Dictation("dict"),
        IntegerRefMF("n", 1, 10),
>>>>>>> Initial multilanguage support
        Choice("control", BINDINGS["control"]),
    ],
    ccr=False,
)

Breathe.add_commands(
    AppContext(executable="scientific notebook"),
    {
        BINDINGS["symbol_prefix"] + " <symbol>": TeX("%(symbol)s"),
        #
<<<<<<< HEAD
        BINDINGS["greek_prefix"] + " [<big>] <greek_letter>": Function(greek),
        BINDINGS["accent_prefix"] + " <accent>": Key("%(accent)s"),
        BINDINGS["unit_prefix"] + " <units>": Alternating("units"),
        "<misc_sn_keys>": Key("%(misc_sn_keys)s"),
        "<misc_sn_text>": Text("%(misc_sn_text)s"),
        "matrix <rows> by <cols>": Function(matrix),
        "<numbers>": Text("%(numbers)s"),
        "<numbers> <denominator>": Key("c-f")
        + Text("%(numbers)s")
        + Key("down")
        + Text("%(denominator)s")
        + Key("right"),
    },
    [
        IntegerRef("rows", 1, BINDINGS["max_matrix_size"]),
        IntegerRef("cols", 1, BINDINGS["max_matrix_size"]),
        IntegerRefMF("numbers", 0, CORE["numbers_max"]),
        Choice("big", {CORE["capitals_prefix"]: True}, default=False),
        Choice("greek_letter", BINDINGS["greek_letters"]),
        Choice("units", BINDINGS["units"]),
        Choice("symbol", BINDINGS["tex_symbols"]),
        Choice("accent", BINDINGS["accents"]),
        Choice("misc_sn_keys", BINDINGS["misc_sn_keys"]),
        Choice("misc_sn_text", BINDINGS["misc_sn_text"]),
        Choice("denominator", BINDINGS["denominators"]),
    ],
)


Breathe.add_commands(
    AppContext(executable="scientific notebook"),
    {
        "[<before>] integral from <sequence1> to <sequence2>": Exec("before")
        + TeX("int")
        + Key("c-l")
        + Exec("sequence1")
        + Key("right, c-h")
        + Exec("sequence2")
        + Key("right"),
        "[<before>] definite from <sequence1> to <sequence2>": Exec("before")
        + Key("c-6, right, c-l")
        + Exec("sequence1")
        + Key("right, c-h")
        + Exec("sequence2")
        + Key("right, c-left, left"),
        "[<before>] differential <sequence1> by <sequence2>": Exec("before")
        + Key("c-f")
        + TeX("partial")
        + Exec("sequence1")
        + Key("down")
        + TeX("partial")
        + Exec("sequence2")
        + Key("right"),
        "[<before>] sum from <sequence1> to <sequence2>": Exec("before")
        + Key(
            "f10, i, down:11, enter/25, a, enter, f10, i, down:11, enter/25, b, enter"
        )
        + TeX("sum")
        + Key("down")
        + Exec("sequence1")
        + Key("up:2")
        + Exec("sequence2")
        + Key("right"),
        "[<before>] limit from <sequence1> to <sequence2>": Exec("before")
        + Key("f10, i, down:11, enter/25, b, enter")
        + TeX("lim")
        + Key("down")
        + Exec("sequence1")
        + TeX("rightarrow")
        + Exec("sequence2")
        + Key("right"),
        "[<before>] argument that <minmax> <sequence1>": Exec("before")
        + Key("f10, i, down:11, enter/25, b, enter")
        + Text("arg%(minmax)s")
        + Key("down")
        + Exec("sequence1")
        + Key("right"),
        "[<before>] <minmax> by <sequence1>": Exec("before")
        + Key("f10, i, down:11, enter/25, b, enter")
        + Text("%(minmax)s")
        + Key("down")
        + Exec("sequence1")
        + Key("right"),
        "[<before>] <script1> <singleton1> [<after>]": Exec("before")
        + Key("%(script1)s")
        + Exec("singleton1")
        + Key("right")
        + Exec("after"),
        "[<before>] <script1> <singleton1> <script2> <singleton2> [<after>]": Exec(
            "before"
        )
        + Key("%(script1)s")
        + Exec("singleton1")
        + Key("right, %(script2)s")
        + Exec("singleton2")
        + Key("right")
        + Exec("after"),
    },
    [
        Choice(
            "minmax", {"(minimum | minimises)": "min", "(maximum | maximises)": "max"}
        ),
        Choice("script1", {"sub": "c-l", "super": "c-h"}),
        Choice("script2", {"sub": "c-l", "super": "c-h"}),
        CommandsRef("before", 8),
        CommandsRef("after", 8),
        CommandsRef("singleton1", 1),
        CommandsRef("singleton2", 1),
        CommandsRef("sequence1", 4),
        CommandsRef("sequence2", 4),
    ],
    top_level=True,
)
=======
        BINDINGS["greek_prefix"] + " [<big>] <greek_letter>":
            Function(greek),
        BINDINGS["accent_prefix"] + " <accent>":
            Key("%(accent)s"),

        BINDINGS["unit_prefix"] + " <units>":
            Alternating("units"),

        "<misc_sn_keys>":
            Key("%(misc_sn_keys)s"),
        "<misc_sn_text>":
            Text("%(misc_sn_text)s"),

        "matrix <rows> by <cols>":
            Function(matrix),

        "<numbers> <denominator>":
            Key("c-f") + Text("%(numbers)s") + Key("down") + Text("%(denominator)s") + Key("right"),
    }

    extras = [
        IntegerRefMF("rows",    1, BINDINGS["max_matrix_size"]),
        IntegerRefMF("cols",    1, BINDINGS["max_matrix_size"]),
        IntegerRefMF("numbers", 0, CORE["numbers_max"]),
        Choice("big",           {CORE["capitals_prefix"]: True}),
        Choice("greek_letter",   BINDINGS["greek_letters"]),
        Choice("units",          BINDINGS["units"]),
        Choice("symbol",         BINDINGS["tex_symbols"]),
        Choice("accent",         BINDINGS["accents"]),
        Choice("misc_sn_keys",   BINDINGS["misc_sn_keys"]),
        Choice("misc_sn_text",   BINDINGS["misc_sn_text"]),
        Choice("denominator",    BINDINGS["denominators"]),
    ]

    defaults = {
        "big": False,
    }

control.nexus().merger.add_app_rule(sn_mathematics())
>>>>>>> Initial multilanguage support
