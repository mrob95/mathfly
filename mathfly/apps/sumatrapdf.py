from mathfly.imports import *

Breathe.add_commands(
	AppContext(title="SumatraPDF"),
	mapping = {
		# https://www.sumatrapdfreader.org/manual.html
		"open file"           : Key("c-o"),
		"print file"          : Key("c-p"),

		"close tab"           : Key("c-w"),
		"next tab"            : Key("c-tab"),
		"previous tab"        : Key("cs-tab"),
		"<nth> tab"           : Key("a-%(nth)s"),

		"go to page"          : Key("c-g"),
		"find"                : Key("c-f"),
		"find next"           : Key("f3"),
		"find previous"       : Key("s-f3"),
		"page <n1000>"        : Key("c-g") + Text("%(n1000)s") + Key("enter"),
		"table of contents"   : Key("f12"),

		"zoom in"             : Key("c-equals"),
		"zoom out"            : Key("c-minus"),
		"fit page"            : Key("c-0"),
		"actual size"         : Key("c-1"),
		"fit width"           : Key("c-2"),
		"fit content"         : Key("c-3"),
		"[view] single page"  : Key("c-6"),
		"facing view"         : Key("c-7"),
		"book view"           : Key("c-8"),
		"rotate [right]"      : Key("c-plus"),
		"rotate left"         : Key("c-minus"),
		"presentation [mode]" : Key("f11"),
		"full screen"         : Key("s-f11"),
	},
	extras = [
		IntegerRef("n1000", 1, 1000),
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
	],
	ccr=False
)