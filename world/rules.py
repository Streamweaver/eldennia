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

    Returns: Boolean

    """
    return roll_dice(2,6) + get_mod(attrib) + mods > 7

def resolve_combat_round(combat_handler):
    """
    Resolves the outcome of actions in a single combat round.
    Args:
        combat_handler: instance of combat_handler

    """
    ch = combat_handler
    # Actions
    ranged_defense = defaultdict(int)
    ranged_bonus = defaultdict(int)
    melee_defense = defaultdict(int)
    melee_bonus = defaultdict(int)
    ranged_attacks = defaultdict(list)
    melee_attacks = defaultdict(list)
    moves = {}

    # Iterate over character action queues and sort by resolution.
    for dbref, queue in ch.db.turn_actions.iteritems():
        for item in queue:
            action, char, target = item
            # Resolve position Changes in order Kite and Rush
            if action == 'retreat':
                moves[dbref] = resolve_move(ch, char, target, -1)
            if action == 'rush':
                moves[dbref] = resolve_move(ch, char, target, 1)
            # Add ranged bonus
            if action == 'aim':
                ranged_bonus[char.id] += 1
            # Add melee bonus
            # Add ranged defense
            if action == 'cover':
                ranged_defense[char.id] += 1
            # Add Melee defense
            if action == 'block':
                melee_defense[char.id] += 1
            # Add ranged attack
            if action == 'shoot':
                ranged_attacks[char.id].append((char, target))
            # Add melee attack
            if action == 'strike':
                melee_attacks[char.id].append((char, target))

    # # resolve ranged
    # for i in range(3): # through each of 3 max rounds
    #     for attack in ranged_attacks.values():
    #         for attacker, defender in attack[i] if len(attack) > i else None:
    #             ok = simple_check(attacker.dex(), ranged_defense[defender.id])
    #             if ok:
    #                 ch.msg_all("%s shoots and hits %s" % (attacker, defender))
    #             else:
    #                 ch.msg_all("%s shoots and misses %s" % (attacker, defender))
    # # resolve melee
    # for i in range(3):
    #     for attack in melee_attacks.values():
    #         for attacker, defender in attack[i] if len(attack) > i else None:
    #             ok = simple_check(attacker.str(), melee_defense[defender.id])
    #             if ok:
    #                 ch.msg_all("%s swings and hits %s" % (attacker, defender))
    #             else:
    #                 ch.msg_all("%s swings and misses %s" % (attacker, defender))

def resolve_move(ch, char, target, mv=1):
    """
    Resolves the action of a single move between char and target in a combat.

    Args:
        ch (CombatHandler): Combat Handler to move in.
        char (Character): Character moving
        target (Character): Target to move against.
        mv (Int): 1 for foward -1 for back

    Returns: Boolean of weather move actually happened.

    """
