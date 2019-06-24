from mathfly.imports import *

class WordPadRule(MergeRule):
	pronunciation = "WordPad"
	mcontext = AppContext(title="WordPad")

	mapping = {
		"new file"            : Key("c-n"),
		"open file"           : Key("c-o"),
		"print file"          : Key("c-p"),

		"page down [<n>]"     : Key("c-pagedown:%(n)s"),
		"page up [<n>]"       : Key("c-pageup:%(n)s"),
	}

	extras = [
		IntegerRef("n", 1, 1000),
	]

	defaults = {
		"n": 1,
	}

control.nexus().merger.add_non_ccr_app_rule(WordPadRule())
