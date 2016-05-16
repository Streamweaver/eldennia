from evennia.contrib.dice import roll_dice

def get_mod(val):
    "Looks up val and returns mod, defaults to zero if can't fine.  Dirty but I couldn't extract a smooth equation."
    mods = {
        0: -3,
        1: -2,
        2: -2,
        3: -1,
        4: -1,
        5: -1,
        9: 1,
        10: 1,
        11: 1,
        12: 2,
        13: 2,
        14: 2,
        15: 3
    }
    return mods.get(val, 0)

def simple_check(attrib, mods=0):
    """
    Produces a task check for attribute value with mods against standard value of 8

    Args:
        attrib (Int): Attribute value
        mods (Int):  modifier for basic roll

    Returns: Boolean of feather successful roll.

    """
    return roll_attribute(attrib, mods) > 7

def roll_attribute(attrib, mods=0):
    """
    Produces the results of a 2d6 plus attribute mod
    Args:
        attrib (Int): Attribute value
        mods (Int): Additional modifiers

    Returns: Int of result

    """
    return roll_dice(2, 6) + get_mod(attrib) + mods

def get_effect(value):
    return value - 8


