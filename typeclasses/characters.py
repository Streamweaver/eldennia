"""
Characters

Characters are (by default) Objects setup to be puppeted by Players.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
from evennia import DefaultCharacter

STATS = {
    'agl': {
        'name': 'Agility',
        'default': 10,
        'desc': "desc"
    },
    'end': {
        'name': 'Endurance',
        'default': 10,
        'desc': "desc"
    },
    'int': {
        'name': 'Intelligence',
        'default': 10,
        'desc': "desc"
    },
    'lck': {
        'name': 'Luck',
        'default': 10,
        'desc': "desc"
    },
    'per': {
        'name': 'Personality',
        'default': 10,
        'desc': "desc"
    },
    'spd': {
        'name': 'Speed',
        'default': 10,
        'desc': "desc"
    },
    'str': {
        'name': 'Strength',
        'default': 10,
        'desc': "desc"
    },
    'wil': {
        'name': 'Willpower',
        'default': 10,
        'desc': "desc"
    }
}

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
        self.db.agl = 10
        self.db.end = 10
        self.db.int = 10
        self.db.lck = 10
        self.db.per = 10
        self.db.spd = 10
        self.db.str = 10
        self.db.wil = 10

        # Static Attributes
        self.db.level = 1
        self.db.gold = 0

        # Derived Attributes
        self.db.health = 1
        self.db.wounds = 0
        self.db.mana = 1
        self.db.drain = 0
        self.db.stamina = 1
        self.db.fatigue = 0

    # Attributes
    def agl(self):
        "Returns effective agility"
        return int(self.db.agl)

    def end(self):
        return int(self.db.end)

    def int(self):
        return int(self.db.end)

    def lck(self):
        return int(self.db.lck)

    def per(self):
        return int(self.db.per)

    def spd(self):
        return int(self.db.spd)

    def str(self):
        return int(self.db.str)

    def wil(self):
        return int(self.db.wil)

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
