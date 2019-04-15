from ctrl.nexus import Nexus

MF_NEXUS = None


def nexus():
    global MF_NEXUS
    if MF_NEXUS is None:
        MF_NEXUS = Nexus()
    return MF_NEXUS
