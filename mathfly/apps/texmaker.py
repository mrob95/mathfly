from mathfly.imports import *

class TeXMakerRule(MergeRule):
	pronunciation = "Tech Maker"
	mcontext = AppContext(executable="texmaker.exe")

	mapping = {
		"new file"            : Key("c-n"),
		"open file"           : Key("c-o"),
		"print file"          : Key("c-p"),

		"find"                : Key("c-f"),
		"find next"           : Key("c-m"),

		"zoom in"             : Key("c-equals"),
		"zoom out"            : Key("c-minus"),

		"quick build": Key("f1"),
		"view PDF": Key("f7"),
	}

	extras = [
		IntegerRef("n", 1, 1000),
		Choice("nth", {
			"first"         : "1",
			"second"        : "2",
			"third"         : "3",
			"fourth"        : "4",
			"fifth"         : "5",
			"sixth"         : "6",
			"seventh"       : "7",
			"eighth"        : "8",
			"(last | final)": "9",
			})
	]

	defaults = {
		"n": 1,
	}

control.nexus().merger.add_non_ccr_app_rule(TeXMakerRule())
