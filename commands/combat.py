from commands.command import MuxCommand
from evennia import create_script
from evennia import CmdSet, default_cmds

class CmdAttack(MuxCommand):
    """
    initiates combat

    Usage:
      attack <target>

    This will initiate combat with <target>. If <target is
    already in combat, you will join the combat.
    """
    key = "attack"
    help_category = "General"

    def func(self):
        "Handle command"
        if not self.args:
            self.caller.msg("Usage: attack <target>")
            return
        target = self.caller.search(self.args)
        if not target:
            return
        # set up combat
        if target.ndb.combat_handler:
            # target is already in combat - join it
            target.ndb.combat_handler.msg_all("%s joins combat!" % self.caller)
            target.ndb.combat_handler.add_character(self.caller)

        else:
            # create a new combat handler
            self.caller.msg("You attack %s! You are in combat." % target)
            target.msg("%s attacks you! You are in combat." % self.caller)
            ch = create_script("combat_handler.CombatHandler")
            ch.add_character(self.caller)
            ch.add_character(target)
            ch.msg_positions(self.caller) # First char added doesn't get anyone's position since they don't exist

class CmdRush(MuxCommand):
    """
    Approch Enemy.

    Usage:
        rush <target>

    Attempts to close the distance to the enemy by one interval.
    """
    key = "rush"
    aliases = []
    help_category = "combat"

    def func(self):
        if not self.args:
           self.caller.msg("Usage: rush <target>")
           return
        target = self.caller.search(self.args)
        if not target:
            return

        ok = self.caller.ndb.combat_handler.add_action("rush",
                                                       self.caller,
                                                       target)
        if ok:
            self.caller.msg("You try to move closer to %s" % target)
        else:
            self.caller.msg("You can only queue 3 actions in a round.")

class CombatCmdSet(CmdSet):
    key = "combat_cmdset"
    mergetype = "Replace"
    priority = 10
    no_exits = True

    def at_cmdset_creation(self):
        self.add(CmdRush())
        # self.add(CmdDisengage())
        # self.add(CmdHelp())
        self.add(default_cmds.CmdPose())
        self.add(default_cmds.CmdSay())