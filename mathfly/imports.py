'''
from mathfly.imports import *
'''

from dragonfly import Dictation, MappingRule, Choice, Function, ContextAction, Repetition, Compound
from dragonfly import Repeat, Playback, Mimic, Window, Clipboard, IntegerRef, ShortIntegerRef
from dragonfly import DictList, DictListRef

from breathe import Breathe, CommandContext, CommandsRef, Exec

from mathfly.lib.actions import Text, Key, Mouse, AppContext
from mathfly.lib.integers import IntegerRefMF

from mathfly.lib import utilities, execution, navigation
from mathfly.lib.latex import tex_funcs
from mathfly.lib.execution import Alternating

import re, os, datetime, sys
from subprocess import Popen