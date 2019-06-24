from mathfly.imports import *

class RuleNameRule(MergeRule):
	pronunciation = "AppName"
	mcontext = AppContext(title="AppName")

	mapping = {
		"new file"            : Key("c-n"),
		"open file"           : Key("c-o"),
		"print file"          : Key("c-p"),

		"close tab"           : Key("c-w"),
		"next tab"            : Key("c-tab"),
		"previous tab"        : Key("cs-tab"),
		"<nth> tab"           : Key("a-%(nth)s"),

		"find"                : Key("c-f"),
		"find next"           : Key("f3"),
		"find previous"       : Key("s-f3"),

		"zoom in"             : Key("c-equals"),
		"zoom out"            : Key("c-minus"),
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

control.nexus().merger.add_non_ccr_app_rule(RuleNameRule())
