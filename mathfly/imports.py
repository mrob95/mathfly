'''
from mathfly.imports import *
'''

from dragonfly import Dictation, MappingRule, Choice, Function, ContextAction, Repetition, Compound
from dragonfly import Repeat, Playback, Mimic, Window, Clipboard, IntegerRef, ShortIntegerRef

from mathfly.lib.actions import Text, Key, Mouse, AppContext
from mathfly.lib.integers import IntegerRefMF

from mathfly.lib import control, utilities, execution, navigation
from mathfly.lib.latex import tex_funcs
from mathfly.lib.execution import Alternating

from mathfly.lib.merge.mergerule import MergeRule
from mathfly.lib.merge.nestedrule import NestedRule
from mathfly.lib.merge.selfmodrule import SelfModifyingRule

import re, os, datetime, sys
from subprocess import Popen