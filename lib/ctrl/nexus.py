from dragonfly.grammar.grammar_base import Grammar
from dragonfly.grammar.recobs import RecognitionHistory

from lib.dfplus.communication import Communicator
from lib.dfplus.merge.ccrmerger import CCRMerger


class Nexus:
    def __init__(self, real_merger_config=True):

        # self.state = CasterState()

        self.clip = {}

        self.history = RecognitionHistory(20)
        self.history.register()

        self.preserved = None

        from dragonfly.timer import _Timer
        self.timer = _Timer(0.025)

        self.comm = Communicator()

        self.macros_grammar = Grammar("recorded_macros")

        self.merger = CCRMerger(real_merger_config)


_NEXUS = None


def nexus():
    global _NEXUS
    if _NEXUS is None:
        _NEXUS = Nexus()
    return _NEXUS
