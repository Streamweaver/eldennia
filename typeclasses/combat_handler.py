from random import randint
from enum import IntEnum

from evennia import DefaultScript

from world import rules

MSG_AUTO_TURN_END = "Turn ending automatically.  Continuing ..."
MSG_TURN_END = "{M Next turn begins!  Choose 3 actions ..."

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

        self.db.characters = {}
        self.db.distance_max = Distance.Extreme
        self.db.distance_min = Distance.Close
        self.db.positions = {}
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
        del self.db.positions[dbref]
        for combatant in self.db.positions.values():
            del combatant[dbref]
        character.cmdset.delete("commands.combat.CombatCmdSet")
        character.msg("You are no longer in combat.")

    def add_character(self, character):
        "Add character to combat"
        dbref = character.id
        self.db.positions[dbref] = {}
        for combatant in self.db.characters.values():
            pos = randint(self.db.distance_min, self.db.distance_max)
            self.db.positions[dbref][combatant.id] = pos
            self.db.positions[combatant.id][dbref] = pos
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
        if 0 <= len(queue) <= 2:  # only allow 3 actions
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
        if all(len(actions) == 3 for actions in self.db.actions.values()):
            self.at_repeat("endturn")

    def end_turn(self):
        if len(self.db.characters) < 2:
            self.msg_all("Combat has ended.")
            self.stop()
        else:
            # Resolve actions
            # rules.resolve_combat_round(self) should go in else
            for dbref in self.db.actions.keys():
                self.db.actions[dbref] = []
            self.msg_all(MSG_TURN_END)

    #--- MOVEMENT
    def set_distance(self, dmax=Distance.Extreme, dmin=Distance.Close):
        """
        Sets the values for the boundaries of relative distance for combatants in the
        combat space.

        Args:
            dmax: int of maxium distance
            dmin: int of minimum distance

        """
        if dmax <= dmin:
            raise CombatHandlerExecption("Distances supplied are invalid.")
        if dmax > Distance.Extreme:
            raise CombatHandlerExecption("Max distance execeeds range")
        if dmin < Distance.Personal:
            raise CombatHandlerExecption("Min distance exceeds range")

        # Set distance boundaries
        self.db.distance_max = dmax
        self.db.distance_min = dmin

        # If character current distances violate this, modify them.  Edge case of morphing
        # rooms.
        for cref, positions in self.db.positions.iteritems():
            for tref, distance in positions.iteritems():
                distance = self.db.positions[cref][tref]
                if distance > self.db.distance_max:
                    self.db.positions[cref][tref] = self.db.distance_max
                if distance < self.db.distance_min:
                    self.db.positions[cref][tref] = self.db.distance_min

    def adjust_position(self, dbref1, dbref2, change):
        """
        Adjusts relative position of two combatants

        Args:
            dbref1:  dbref of  chracter 1
            dbref2:  dbref of character 2
            change: int of distance increment to change range, positive or negative

        Return:  Boolean of weather the position was actually changed.  False if ecxeeds boundaries.

        """
        new_position = self.db.positions[dbref1][dbref2] + change
        if new_position > self.db.distance_max:
            return False
        if new_position < self.db.distance_min:
            return False
        self.db.positions[dbref1][dbref2] = new_position
        self.db.positions[dbref2][dbref1] = new_position
        return True

    def get_distance(self, dbref1, dbref2):
        """
        Returns the relative position of two characters.

        Args:
            dbref1: dbref of char1
            dbref2: dbref of char2

        Returns: Int of relative distance between characters.

        """
        try:
            return self.db.positions[dbref1][dbref2]
        except KeyError:
            raise CombatHandlerExecption("Character with dbref does not have a position")

    def msg_positions(self, character):
        """
        Messages each combatant with the names of other combatants and their relative positions.

        Args:
            character (Character): char object to message

        """
        # positions = [[self.db.characters[tid], pos] for tid, pos in self.db.positions[character.id].iteritems()]
        positions = []
        for tid, pos in self.db.positions[character.id].iteritems():
            positions.append("%s(%s)" % (self.db.characters[tid], Distance(pos).name))
        if positions:
            plural = "s" if len(positions) > 1 else ""
            character.msg("Target%s(Range): " % plural + ", ".join(positions))
