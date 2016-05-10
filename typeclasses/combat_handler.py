from random import randint
from enum import IntEnum

from evennia import DefaultScript

from world import rules

class Distance(IntEnum):
    Personal = 0
    Close = 1
    Short = 2
    Medium = 3
    Long = 4
    Far = 5
    Extreme = 6

class Direction(IntEnum):
    Back = -1
    Steady = 0
    Forward = 1

class CombatHandler(DefaultScript):
    """
    Simple combat handler.
    """

    def at_script_creation(self):
        self.key = "cbt_hlr_%s" % hex(randint(1, 10000))
        self.des = "handles combat"
        self.interval = 60 * 2 # one min timeout
        self.start_delay = True
        self.persistant = True

        self.db.characters = {}
        self.db.positions = {}
        self.db.turn_actions = {}

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
        del self.db.turn_actions[dbref]
        del character.ndb.combat_handler
        del self.db.positions[dbref]
        for combatant in self.db.positions.values():
            del combatant[dbref]
        character.cmdset.delete("commands.combat.CombatCmdSet")
        character.msg("You are no longer in combat.")

    def at_start(self):
        "called at start and after server reboot"
        for character in self.db.characters.values():
            self._init_character(character)

    def at_stop(self):
        "Called just before script stopped or destroyed."
        for character in list(self.db.characters.values()):
            # note list() so handles disconnected characters.
            self._cleanup_character(character)

    def at_repeat(self, *args):
        """
        Called every self.interval seconds or when all characters fill queue.

        We let this method take optional arguments (using *args) so we can separate
        between the timeout (no argument) and the controlled turn-end
        where we send an argument.
        """
        if not args:
            self.msg_all("Turn ending automatically.  Continuing ...")
        self.end_turn()

    def add_character(self, character):
        "Add character to combat"
        dbref = character.id
        self.db.positions[dbref] = {}
        for combatant in self.db.characters.values():
            pos = randint(0, 6)
            self.db.positions[dbref][combatant.id] = pos
            self.db.positions[combatant.id][dbref] = pos
        self.db.characters[dbref] = character
        self.db.turn_actions[dbref] = []
        self._init_character(character)
        self.msg_positions(character)

    def remove_character(self, character):
        if character.id in self.db.characters:
            self._cleanup_character(character)
        if not self.db.characters:
            self.stop() # End of nobody left.

    def msg_all(self, message):
        "Send message to all participants"
        for character in self.db.characters.values():
            character.msg(message)

    def adjust_position(self, char, tar, pos):
        """
        Adjusts relative position of two combatants
        Args:
            char: character object
            tar: target object
            pos: int of position adjustment

        Return: Int of position change
        """
        updated = self.db.positions[char.id][tar.id] + pos
        if 0 <= updated <= 6:
            self.db.positions[char.id][tar.id] = updated
            self.db.positions[tar.id][char.id] = updated
            return True
        return False

    def add_action(self, action, character, target):
        """
        Call by combat commands to register an action for the turn.
        Args:
            action: string of action name
            character: character object
            target: character object

        """
        queue = self.db.turn_actions[character.id]
        if 0 <= len(queue) <= 2: # only allow 3 actions
            queue.append((action, character, target))
            self._check_end_turn() # check if everyone has entered commands
            return True
        else:
            return False

    def _check_end_turn(self):
        if all(len(actions) == 3 for actions in self.db.turn_actions.values()):
            self.at_repeat("endturn")

    def end_turn(self):

        rules.resolve_combat_round(self)
        if len(self.db.characters) < 2:
            self.msg_all("Combat has ended.")
            self.stop()
        else:
            # clear character turn actions
            self.msg_all("{M Next turn begins!  Choose 3 actions ...")
            for character in self.db.characters.values():
                self.db.turn_actions[character.id] = []
                self.msg_positions(character)

    def msg_positions(self, character):
        """
        Messages each combatant with the names of other combatants and their relative positions.

        Args:
            character (Character): char object to message

        """
        # positions = [[self.db.characters[tid], pos] for tid, pos in self.db.positions[character.id].iteritems()]
        positions = []
        for tid, pos in self.db.positions[character.id].iteritems():
            if tid != character.id:
                dst = "%s" % Distance(pos).name
                positions.append("%s(%s)" % (self.db.characters[tid], dst))
        if positions:
            character.msg("Target(Range): " + ", ".join(positions))


