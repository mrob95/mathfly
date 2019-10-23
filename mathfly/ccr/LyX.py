'''
Created Jan 2019

@author: Mike Roberts, Alex Boche
'''
from mathfly.imports import *

BINDINGS = utilities.load_toml_relative("config/lyx.toml")
CORE     = utilities.load_toml_relative("config/core.toml")

def greek(big, greek_letter):
    if big:
        greek_letter = greek_letter.title()
    Text("\\" + greek_letter + " ").execute()

def matrix(rows, cols):
    Text("\\" + BINDINGS["matrix_style"] + " ").execute()
    Key("a-m, w, i, "*(rows-1) + "a-m, c, i, "*(cols-1)).execute()

Breathe.add_commands(
    AppContext(executable="lyx.exe"),
    {
        "<control>": Key("%(control)s"),
        "<control_repeat> [<n>]": Key("%(control_repeat)s") * Repeat("n"),
    },
    [
        Choice("control", BINDINGS["control"]),
        Choice("control_repeat", BINDINGS["control_repeat"]),
    ],
    ccr=False,
)

Breathe.add_commands(
    AppContext(executable="lyx.exe"),
    {
        "<numbers>": Text("%(numbers)s"),
        BINDINGS["symbol1_prefix"] + " <symbol1>": Text("\\%(symbol1)s "),
        BINDINGS["symbol2_prefix"] + " <symbol2>": Text("\\%(symbol2)s "),
        BINDINGS["accent_prefix"] + " <accent>": Key("a-m, %(accent)s"),
        BINDINGS["text_prefix"] + " <text_modes>": Text("\\%(text_modes)s "),
        BINDINGS["greek_prefix"] + " [<big>] <greek_letter>": Function(greek),
        "<misc_lyx_keys>": Key("%(misc_lyx_keys)s"),
        "<command>": Alternating("command"),
        "matrix <rows> by <cols>": Function(matrix),
        "<numbers> <denominator>": Key(
            "a-m, f, %(numbers)s, down, %(denominator)s, right"
        ),
    },
    [
        IntegerRef("rows", 1, BINDINGS["max_matrix_size"]),
        IntegerRef("cols", 1, BINDINGS["max_matrix_size"]),
        IntegerRef("numbers", 0, CORE["numbers_max"]),
        Choice("big", {CORE["capitals_prefix"]: True}, default=False),
        Choice("greek_letter", BINDINGS["greek_letters"]),
        Choice("symbol1", BINDINGS["tex_symbols1"]),
        Choice("symbol2", BINDINGS["tex_symbols2"]),
        Choice("accent", BINDINGS["accents"]),
        Choice("text_modes", BINDINGS["text_modes"]),
        Choice("misc_lyx_keys", BINDINGS["misc_lyx_keys"]),
        Choice("command", BINDINGS["misc_lyx_commands"]),
        Choice("denominator", BINDINGS["denominators"]),
    ],
)


Breathe.add_commands(
    AppContext(executable="lyx.exe"),
    {
        "[<before>] integral from <sequence1> to <sequence2>": Exec("before")
        + Text("\\int _")
        + Exec("sequence1")
        + Key("right, caret")
        + Exec("sequence2")
        + Key("right"),
        "[<before>] definite from <sequence1> to <sequence2>": Exec("before")
        + Key("a-m, lbracket, right, underscore")
        + Exec("sequence1")
        + Key("right, caret")
        + Exec("sequence2")
        + Key("right, left:2"),
        "[<before>] differential <sequence1> by <sequence2>": Exec("before")
        + Key("a-m, f, d")
        + Exec("sequence1")
        + Key("down, d")
        + Exec("sequence2")
        + Key("right"),
        "[<before>] sum from <sequence1> to <sequence2>": Exec("before")
        + Text("\\stackrelthree ")
        + Key("down")
        + Text("\\sum ")
        + Key("down")
        + Exec("sequence1")
        + Key("up:2")
        + Exec("sequence2")
        + Key("right"),
        "[<before>] limit from <sequence1> to <sequence2>": Exec("before")
        + Text("\\underset \\lim ")
        + Key("down")
        + Exec("sequence1")
        + Text("\\rightarrow ")
        + Exec("sequence2")
        + Key("right"),
        "[<before>] argument that <minmax> <sequence1>": Exec("before")
        + Text("\\underset \\arg \\%(minmax)s ")
        + Key("down")
        + Exec("sequence1")
        + Key("right"),
        "[<before>] <minmax> by <sequence1>": Exec("before")
        + Text("\\underset \\%(minmax)s ")
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
    extras=[
        Choice(
            "minmax", {"(minimum | minimises)": "min", "(maximum | maximises)": "max"}
        ),
        Choice("script1", {"sub": "_", "super": "^"}),
        Choice("script2", {"sub": "_", "super": "^"}),
        CommandsRef("before", 8),
        CommandsRef("after", 8),
        CommandsRef("singleton1", 1),
        CommandsRef("singleton2", 1),
        CommandsRef("sequence1", 4),
        CommandsRef("sequence2", 4),
    ],
    top_level=True,
)

