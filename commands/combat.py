from commands.command import MuxCommand
from evennia import create_script
from evennia import CmdSet, default_cmds

MAX_COMMANDS = 2
MSG_MAX_COMMANDS = "You can only queue %i actions in a turn." % MAX_COMMANDS

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

# Initiative Actions
class CmdRush(MuxCommand):
    """
    Rush your attacks

    Usage:
        rush

    Hurry your actions to gain a bonus to initiative but penalty to all other actions for the round.
    """
    key = "rush"
    aliases = ["hasten", "hurry"]
    locks = "cmd:all()"
    help_category = "combat"

    def func(self):
        ok = self.caller.ndb.combat_handler.add_action(self.key,
                                                       self.caller,
                                                       None)
        if ok:
            self.caller.msg("You rush your attacks recklessly.")
        else:
            self.caller.msg(MSG_MAX_COMMANDS)

# Defensive Actions
class CmdDodge(MuxCommand):
    """
    Actively dodge attacks.

    Usage:
        dodge

    Add Dex modfier to all defenses while taking a penalty to all actions. Lasts remainder of the turn.

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
            self.caller.msg(MSG_MAX_COMMANDS)

class CmdParry(MuxCommand):
    """
    Block incomming melee attacks.

    Usage:
        parry

    Add melee skill to melee defense, take penalty to all other actions.  Lasts until end of turn.

    """
    key = "parry"
    aliases = ["block",]
    locks = "cmd:all()"
    help_category = "combat"

    def func(self):
        ok = self.caller.ndb.combat_handler.add_action(self.key,
                                                       self.caller,
                                                       None)
        if ok:
            self.caller.msg("You %s incoming attacks." % self.key)
        else:
            self.caller.msg(MSG_MAX_COMMANDS)

# Attack bonus actions
class CmdAim(MuxCommand):
    """
    Aim carefully.

    Usage:
        aim

    Add 1 to ranged attack roles for the round.

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
            self.caller.msg(MSG_MAX_COMMANDS)

# Attack Actions
class CmdShoot(MuxCommand):
    """
    Make a ranged attack.

    Usage:
        shoot <target>

    Make a ranged attack with your equipt weapon at target.

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
            self.caller.msg(MSG_MAX_COMMANDS)

class CmdStrike(MuxCommand):
    """
    Make a melee attack.

    Usage:
        strike <target>

    Make a melee attack with your equipt weapon at target.

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
            self.caller.msg("You strike at %s." % target)
        else:
            self.caller.msg(MSG_MAX_COMMANDS)

class CombatCmdSet(CmdSet):
    key = "combat_cmdset"
    mergetype = "Replace"
    priority = 10
    no_exits = True

    def at_cmdset_creation(self):
        self.add(CmdRush())
        self.add(CmdDodge())
        self.add(CmdParry())
        self.add(CmdAim())
        self.add(CmdShoot())
        self.add(CmdStrike())
        # self.add(CmdDisengage())
        # self.add(CmdHelp())
        self.add(default_cmds.CmdPose())
        self.add(default_cmds.CmdSay())