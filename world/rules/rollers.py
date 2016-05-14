from evennia.contrib.dice import roll_dice
from collections import defaultdict

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
    return roll_dice(2,6) + get_mod(attrib) + mods > 7


# Method based implmenetation
# def resolve_combat_round(combat_handler):
#     """
#     Resolves the outcome of actions in a single combat round.
#     Args:
#         combat_handler: instance of combat_handler
#
#     """
#     ch = combat_handler
#     # Actions
#     general_defense = defaultdict(int)
#     ranged_defense = defaultdict(int)
#     ranged_bonus = defaultdict(int)
#     melee_defense = defaultdict(int)
#     melee_bonus = defaultdict(int)
#     ranged_attacks = defaultdict(list)
#     melee_attacks = defaultdict(list)
#     moves = []
#
#     # Iterate over character action queues and sort by resolution.
#     for dbref, queue in ch.db.actions.iteritems():
#         for item in queue:
#             action, char, target = item
#             # Resolve position Changes in order Kite and Rush
#             if action == 'retreat' or action == 'rush':
#                 moves.append(item)
#             if action == 'aim': # Add automatic ranged bonuses
#                 ranged_bonus[char.id] += 1
#             if action == 'cover': # Add automatic ranged defenses
#                 ranged_defense[char.id] += 1
#             if action == 'block':# Add automatic Melee defense
#                 melee_defense[char.id] += 1
#             if action == 'shoot': # Queue a ranged attack
#                 ranged_attacks[char.id].append((char, target))
#             if action == 'strike': # Queue melee attack
#                 melee_attacks[char.id].append((char, target))
#             if action == 'dodge': # Add a general defense if dex check
#                 general_defense[char.id] += 1 if simple_check(char.dex(), -2) else 0
#
#     for item in ch.db.actions.values():
#         action, character, target = item
#         msg = "You %s %s" % (action, target) if target else "You %s" % action
#         character.msg(msg)

    # # resolve moves, update positions and build feedback
    # for msg in set(resolve_moves(ch, moves)):
    #     ch.msg_all(msg)
    #
    # # if melee attacks that can't be made, convert to dodge.
    # mfb, melee_attacks = melee_to_dodge(ch, melee_attacks, general_defense)
    # for msg in mfb:
    #     ch.msg_all(msg)

