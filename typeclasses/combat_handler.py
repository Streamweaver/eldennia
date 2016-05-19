from random import randint
from enum import IntEnum

from evennia import DefaultScript

from world.rules.resolvers import resolve_combat_turn

MSG_AUTO_TURN_END = "Turn ending automatically.  Continuing ..."
MSG_TURN_END = "{M Next turn begins!  Choose 2 actions ..."

class CombatHandlerExecption(Exception):
    pass

class CombatHandler(DefaultScript):
    """
    Simple combat handler.
    """

    def at_script_creation(self):
        self.key = "cmbt_hdlr_%s" % hex(randint(1, 10000))
        self.des = "handles combat"
        self.interval = 60 * 2  # one min timeout
        self.start_delay = True
        self.persistant = True

        self.db.characters = {} # {dbref: Character, ...}
        self.db.actions = {} # {dbref: [('actionstring', caller, target), ...], ...}

    def at_start(self):
        "called at start and after server reboot"
        for character in self.db.characters.values():
            self._init_character(character)

    def at_stop(self):
        "Called just before script stopped or destroyed."
        for character in list(self.db.characters.values()):
            # note list() so handles disconnected characters.
            self._cleanup_character(character)

    def _init_character(self, character):
        """
        Initializes handler back-reference and combat cmdset on a character
        Args:
            character: character object

        Returns: None

        """
        character.ndb.combat_handler = self
        character.cmdset.add("commands.combat.CombatCmdSet")

    def _cleanup_character(self, character):
        """
        Remove character from handler and clean back-reference and cmdset

        Args:
            character: character object

        """
        dbref = character.id
        del self.db.characters[dbref]
        del self.db.actions[dbref]
        del character.ndb.combat_handler
        character.cmdset.delete("commands.combat.CombatCmdSet")
        character.msg("You are no longer in combat.")

    def add_character(self, character):
        "Add character to combat"
        dbref = character.id
        self.db.characters[dbref] = character
        self.db.actions[dbref] = []
        self._init_character(character)

    def remove_character(self, character):
        if character.id in self.db.characters:
            self._cleanup_character(character)
        if not self.db.characters:
            self.stop()  # End of nobody left.

    def msg_all(self, message):
        "Send message to all participants"
        for character in self.db.characters.values():
            character.msg(message)

    # ----- Actions and Turns
    def add_action(self, action, character, target):
        """
        Call by combat commands to register an action for the turn.
        Args:
            action: string of action name
            character: character object
            target: character object

        """
        queue = self.db.actions[character.id]
        if 0 <= len(queue) <= 1:  # only allow 2 actions
            queue.append((action, character, target))
            self._check_end_turn()  # check if everyone has entered commands
            return True
        else:
            return False

    def at_repeat(self, *args):
        """
        Called every self.interval seconds or when all characters fill queue.

        We let this method take optional arguments (using *args) so we can separate
        between the timeout (no argument) and the controlled turn-end
        where we send an argument.
        """
        if not args:
            self.msg_all(MSG_AUTO_TURN_END)
        self.end_turn()

    def _check_end_turn(self):
        if all(len(actions) == 2 for actions in self.db.actions.values()):
            self.at_repeat("endturn")

    def end_turn(self):
        # Resolve actions
        resolve_combat_turn(self)
        for dbref in self.db.actions.keys():
            self.db.actions[dbref] = []
        self.msg_all(MSG_TURN_END)
        for c in self.db.characters.values():
            if c.is_incapacitated():
                self.msg_all("%s is knocked out.")
                self.remove_character(c)
        if len(self.db.characters) < 2:
            self.msg_all("Combat has ended.")
            self.stop()
