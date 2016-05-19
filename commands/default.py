from evennia import default_cmds
from .command import MuxCommand

"""
This overrides evennia default commands to include overrides to the MuxCommand.
"""

class CmdLook(default_cmds.CmdLook, MuxCommand):
    pass
class CmdHome(default_cmds.CmdHome, MuxCommand):
    pass
class CmdInventory(default_cmds.CmdInventory, MuxCommand):
    pass
class CmdPose(default_cmds.CmdPose, MuxCommand):
    pass
class CmdNick(default_cmds.CmdNick, MuxCommand):
    pass
class CmdDesc(default_cmds.CmdDesc, MuxCommand):
    pass
class CmdGet(default_cmds.CmdGet, MuxCommand):
    pass
class CmdDrop(default_cmds.CmdDrop, MuxCommand):
    pass
class CmdGive(default_cmds.CmdGive, MuxCommand):
    pass
class CmdSay(default_cmds.CmdSay, MuxCommand):
    pass
class CmdAccess(default_cmds.CmdAccess, MuxCommand):
    pass
