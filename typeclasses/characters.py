"""
Characters

Characters are (by default) Objects setup to be puppeted by Players.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
from evennia import DefaultCharacter
from evennia.contrib.dice import roll_dice

def _gen_stat():
    """
    Dirty method for random stat generation.

    Returns: int between 2-12

    """
    return max(roll_dice(2, 6), roll_dice(2, 6))

class Character(DefaultCharacter):
    """
    The Character defaults to reimplementing some of base Object's hook methods with the
    following functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead).
    at_after_move - Launches the "look" command after every move.
    at_post_unpuppet(player) -  when Player disconnects from the Character, we
                    store the current location in the pre_logout_location Attribute and
                    move it to a None-location so the "unpuppeted" character
                    object does not need to stay on grid. Echoes "Player has disconnected"
                    to the room.
    at_pre_puppet - Just before Player re-connects, retrieves the character's
                    pre_logout_location Attribute and move it back on the grid.
    at_post_puppet - Echoes "PlayerName has entered the game" to the room.

    """
    def at_object_creation(self):
        # Basic Attributes
        self.db.str = _gen_stat()
        self.db.dex = _gen_stat()
        self.db.end = _gen_stat()
        self.db.int = _gen_stat()
        self.db.edu = _gen_stat()
        self.db.soc = _gen_stat()

        self.db.credits = 0
        # Derived Attributes


    # Attributes
    def str(self):
        "Returns effective agility"
        return int(self.db.str)

    def dex(self):
        return int(self.db.dex)

    def end(self):
        return int(self.db.end)

    def int(self):
        return int(self.db.int)

    def edu(self):
        return int(self.db.edu)

    def soc(self):
        return int(self.db.soc)

    # Derived Attributes
    def health(self):
        v = self.db.health - self.db.wounds
        if v > 0:
            return v
        return 0

    def mana(self):
        v = self.db.mana - self.db.drain
        if v > 0:
            return v
        return 0

    def stamina(self):
        v = self.db.stamina - self.db.fatigue
        if v > 0:
            return v
        return 0
