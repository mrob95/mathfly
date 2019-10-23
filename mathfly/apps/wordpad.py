from mathfly.imports import *

Breathe.add_commands(
	AppContext(title="WordPad"),
	mapping = {
		"new file"            : Key("c-n"),
		"open file"           : Key("c-o"),
		"print file"          : Key("c-p"),

		"page down [<n>]"     : Key("c-pagedown:%(n)s"),
		"page up [<n>]"       : Key("c-pageup:%(n)s"),
	},
)
