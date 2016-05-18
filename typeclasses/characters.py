"""
Characters

Characters are (by default) Objects setup to be puppeted by Players.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
import random
from evennia import DefaultCharacter
from evennia.contrib.dice import roll_dice
from evennia.utils.utils import lazy_property
from ainneve.world.traits import TraitHandler

_stats = ('STR', 'END', 'DEX', 'INT', 'EDU', 'SOC')

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
        self.db.race = None
        self.db.homeworld = None
        self.db.age = 0
        self.db.credits = 0

    @lazy_property
    def stats(self):
        return TraitHandler(self, db_attribute="stats")

    @lazy_property
    def skills(self):
        return TraitHandler(self, db_attribute="skills")

    @lazy_property
    def specializations(self):
        return TraitHandler(self, db_attribute="specializations")

    # Saving this becuse worked out dividing damage up.
    # def add_damage(self, dmg):
    #     # apply to end, if out then random to st or dex
    #     # total damage = total stats then out
    #     for _ in range(dmg):
    #         alt_stats = []
    #         if self.db.dex - self.db.wounds["dex"] > 0:
    #             alt_stats.append("dex")
    #         if self.db.str - self.db.wounds["str"] > 0:
    #             alt_stats.append("str")
    #         if self.db.end - self.db.wounds["end"] > 0:
    #             self.db.wounds["end"] += 1
    #         elif alt_stats:
    #             stat = random.choice(alt_stats)
    #             stat_value = getattr(self.db, stat)
    #             if stat_value - self.db.wounds[stat] > 0:
    #                 self.db.wounds[stat] += 1
    #         else:
    #             break

