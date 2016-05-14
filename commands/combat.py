from commands.command import MuxCommand
from evennia import create_script
from evennia import CmdSet, default_cmds

class CmdAttack(MuxCommand):
    """
    Initiates combat with target

    Usage:
      attack <target>

    This will initiate combat with <target>. Joins combat if you or <target> already in combat.
    """
    key = "attack"
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        "Handle command"
        if not self.args:
            self.caller.msg("Usage: %s <target>" % self.key)
            return
        target = self.caller.search(self.args)
        if not target:
            return

        # Make sure can't be in two different combat handlers at once
        # TODO have a single combat handler for a location
        if self.caller.ndb.combat_handler and target.ndb.combat_handler:
            self.caller.msg("Finish this fight before the next.")
            return

        # set up combat
        if target.ndb.combat_handler: # Join their if they have one
            # target is already in combat - join it
            target.ndb.combat_handler.msg_all("%s joins combat!" % self.caller)
            target.msg("%s attacks you and joins the combat!" % self.caller)
            target.ndb.combat_handler.add_character(self.caller)
        elif self.caller.ndb.combat_handler:
            self.caller.msg("You attack %s and continue combat." % target)
            target.msg("%s attacks you and pulls you into the conflict."
                       % self.caller)
            self.caller.ndb.combat_handler.add_character(target)
        else:
            # create a new combat handler
            self.caller.msg("You attack %s! You are in combat." % target)
            target.msg("%s attacks you! You are in combat." % self.caller)
            ch = create_script("combat_handler.CombatHandler")
            ch.add_character(self.caller)
            ch.add_character(target)
            ch.msg_positions(self.caller) # First char added doesn't get anyone's position since they don't exist

# Move Actions
class CmdRush(MuxCommand):
    """
    Move closer to target.

    Usage:
        rush <target>

    Dex check to move closer to target one interval.

    """
    key = "rush"
    aliases = []
    locks = "cmd:all()"
    help_category = "combat"

    def func(self):
        if not self.args:
            self.caller.msg("Usage: %s <target>" % self.key)
            return

        target = self.caller.search(self.args)
        if not target:
            self.caller.msg("No target found named %s" % self.args)
            return

        ok = self.caller.ndb.combat_handler.add_action(self.key,
                                                       self.caller,
                                                       target)
        if ok:
            self.caller.msg("You try to move closer to %s." % target)
        else:
            self.caller.msg("You can only queue 3 actions in a turn.")

class CmdRetreat(MuxCommand):
    """
    Move away from target.

    Usage:
        retreat <target>

    Dex check to move away from target one interval.

    """
    key = "retreat"
    aliases = ["kite",]
    locks = "cmd:all()"
    help_category = "combat"

    def func(self):
        if not self.args:
            self.caller.msg("Usage: %s <target>" % self.key)
            return
        target = self.caller.search(self.args)
        if not target:
            return
        ok = self.caller.ndb.combat_handler.add_action(self.key,
                                                       self.caller,
                                                       target)
        if ok:
            self.caller.msg("You try to move away from %s." % target)
        else:
            self.caller.msg("You can only queue 3 actions in a turn.")

# Defensive Actions
class CmdDodge(MuxCommand):
    """
    Attempt general defensive dodge against all attack types.

    Usage:
        dodge

    Dex check -2 to add 1 to defense against melee and ranged.

    """
    key = "dodge"
    aliases = []
    locks = "cmd:all()"
    help_category = "combat"

    def func(self):
        ok = self.caller.ndb.combat_handler.add_action(self.key,
                                                       self.caller,
                                                       None)
        if ok:
            self.caller.msg("You try to dodge all attacks.")
        else:
            self.caller.msg("You can only queue 3 actions in a turn.")

class CmdCover(MuxCommand):
    """
    Gain defense against ranged attacks.

    Usage:
        cover

    Automatic +1 to ranged defense.

    """
    key = "cover"
    aliases = []
    locks = "cmd:all()"
    help_category = "combat"

    def func(self):
        ok = self.caller.ndb.combat_handler.add_action(self.key,
                                                       self.caller,
                                                       None)
        if ok:
            self.caller.msg("You duck behind cover.")
        else:
            self.caller.msg("You can only queue 3 actions in a turn.")

class CmdBlock(MuxCommand):
    """
    Gain defense against melee attacks.

    Usage:
        block

    Automatic +1 to melee defense.

    """
    key = "block"
    aliases = ["parry",]
    locks = "cmd:all()"
    help_category = "combat"

    def func(self):
        ok = self.caller.ndb.combat_handler.add_action(self.key,
                                                       self.caller,
                                                       None)
        if ok:
            self.caller.msg("You block incoming attacks.")
        else:
            self.caller.msg("You can only queue 3 actions in a turn.")

# Attack bonus actions
class CmdAim(MuxCommand):
    """
    Gain bonus ranged attacks.

    Usage:
        aim

    Automatic +1 to ranged attacks.

    """
    key = "aim"
    aliases = []
    locks = "cmd:all()"
    help_category = "combat"

    def func(self):
        ok = self.caller.ndb.combat_handler.add_action(self.key,
                                                       self.caller,
                                                       None)
        if ok:
            self.caller.msg("You take time to aim.")
        else:
            self.caller.msg("You can only queue 3 actions in a turn.")

# Attack Actions
class CmdShoot(MuxCommand):
    """
    Gain bonus ranged attacks.

    Usage:
        shoot <target>

    Automatic +1 to ranged attacks.

    """
    key = "shoot"
    aliases = []
    locks = "cmd:all()"
    help_category = "combat"

    def func(self):
        if not self.args:
            self.caller.msg("Usage: %s <target>" % self.key)
            return
        target = self.caller.search(self.args)
        if not target:
            return
        ok = self.caller.ndb.combat_handler.add_action(self.key,
                                                       self.caller,
                                                       target)
        if ok:
            self.caller.msg("You shoot at %s." % target)
        else:
            self.caller.msg("You can only queue 3 actions in a turn.")

class CmdStrike(MuxCommand):
    """
    Gain bonus ranged attacks.

    Usage:
        strike <target>

    Automatic +1 to ranged attacks.

    """
    key = "strike"
    aliases = []
    locks = "cmd:all()"
    help_category = "combat"

    def func(self):
        if not self.args:
            self.caller.msg("Usage: %s <target>" % self.key)
            return
        target = self.caller.search(self.args)
        if not target:
            return
        ok = self.caller.ndb.combat_handler.add_action(self.key,
                                                       self.caller,
                                                       target)
        if ok:
            self.caller.msg("You shoot at %s." % target)
        else:
            self.caller.msg("You can only queue 3 actions in a turn.")

class CombatCmdSet(CmdSet):
    key = "combat_cmdset"
    mergetype = "Replace"
    priority = 10
    no_exits = True

    def at_cmdset_creation(self):
        self.add(CmdRush())
        self.add(CmdRetreat())
        self.add(CmdDodge())
        self.add(CmdCover())
        self.add(CmdBlock())
        self.add(CmdAim())
        self.add(CmdShoot())
        self.add(CmdStrike())
        # self.add(CmdDisengage())
        # self.add(CmdHelp())
        self.add(default_cmds.CmdPose())
        self.add(default_cmds.CmdSay())