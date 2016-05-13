"""
Implements rules related to combat movement.
"""
from random import randint
from enum import IntEnum

class MovementError(Exception):
    pass

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

class RelativePositions:
    """
    Class to track the relative positions of characters or
    entities in a combat and movement of relative postions.

    """

    def __init__(self, max=Distance.Extreme, min=Distance.Close):
        if max > Distance.Extreme:
            raise MovementError("Max distance execeeds range")
        if min < Distance.Personal:
            raise MovementError("Min distance exceeds range")

        self.positions = {}
        self.max_range = max
        self.min_range = min

    def add_character(self, dbref, max=Distance.Extreme, min=Distance.Close):
        """
        Adds a character and records or generates a relative position to every other entity being tracked.

        Args:
            dbref: string of character dB reference add.

        """
        self.positions[dbref.id] = {}
        for target_id, target_list in self.positions.iteritems():
            distance = randint(min, max)
            self.positions[dbref.id][target_id] = distance
            self.positions[target_id][dbref.id] = distance

    def remove_character(self, dbref):
        """
        Removes a character and all their target pairings and references to character in other target lists.

        Args:
            dbref: string of the character db reference to remove.

        """
        del self.positions[dbref]
        for target_id, target_list in self.positions.iteritems():
            del target_list[dbref]

    def change_position(self, char1, char2, change):
        """
        Changes the relative position of two characters by the provided increment as long as it does not
        exceed the min or max for the class.

        Args:
            char1:  dbref of  chracter 1
            char2:  dbref of character 2
            change: int of distance increment to change range, positive or negative

        """
        new_position = self.positions[char1][char2] + change
        if new_position > self.max:
            return False
        if new_position < self.min:
            return False
        self.positions[char1][char2] = new_position
        self.positions[char2][char1] = new_position
        return True

    def get_distance(self, char1, char2):
        """
        Returns the relative position of two characters.

        Args:
            char1: dbref of char1
            char2: dbref of char2

        Returns: Int of relaive distance between characters.

        """
        try:
            return self.positions[char1][char2]
        except KeyError:
            raise MovementError("Character with dbref does not have a position")