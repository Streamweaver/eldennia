from collections import defaultdict

from world.rules.rollers import simple_check
from commands.combat import CmdDodge, CmdBlock, CmdRetreat, CmdAim, CmdCover, CmdRush, CmdShoot, CmdStrike

def resolve_combat_turn(combat_handler):
    """
    Resolves the outcome of actions in a single combat round.
    Args:
        combat_handler: instance of combat_handler

    """
    ch = combat_handler
    # Actions
    general_defense = defaultdict(int)
    ranged_defense = defaultdict(int)
    ranged_bonus = defaultdict(int)
    melee_defense = defaultdict(int)
    melee_bonus = defaultdict(int)
    ranged_attacks = defaultdict(list)
    melee_attacks = defaultdict(list)
    moves = []

    # Iterate over character action queues and sort by resolution.
    for dbref, queue in ch.db.actions.iteritems():
        for item in queue:
            action, char, target = item
            # Resolve position Changes in order Kite and Rush
            if action == CmdRetreat.key or action == CmdRush.key:
                moves.append(item)
            if action == CmdAim.key: # Add automatic ranged bonuses
                ranged_bonus[char.id] += 1
            if action == CmdCover.key: # Add automatic ranged defenses
                ranged_defense[char.id] += 1
            if action == CmdBlock.key:# Add automatic Melee defense
                melee_defense[char.id] += 1
            if action == CmdShoot.key: # Queue a ranged attack
                ranged_attacks[char.id].append((char, target))
            if action == CmdStrike.key: # Queue melee attack
                melee_attacks[char.id].append((char, target))
            if action == CmdDodge.key: # Add a general defense if dex check
                general_defense[char.id] += 1 if simple_check(char.dex(), -2) else 0

    for queue in ch.db.actions.values():
        for item in queue:
            action, character, target = item
            msg = "You %s %s." % (action, target) if target else "You %s." % action
            character.msg(msg)

def resolve_ranged_attacks():
    pass
def resolve_melee_attacks():
    pass

def melee_to_dodge(ch, melee_attacks, general_defense):
    """
    Any queue melee attacks on out of range opponents are converted to dodges.
    Args:
        ch (CombatHandler): ch instance for fight.
        melee_attacks (dict): dbref: [(char, target)] of character making attack.
        general_defense (defaultdict(int)):  dbref: int of char and their defense bonus

    Return:  (Tuple) (
            List of strings with dodge feedback.
            Defaultdict(list) of actual melee attacks
            )

    """
    feedback = []
    remaining_attacks = defaultdict(list)
    for dbref, attacks in melee_attacks.iteritems():
        for attack in attacks: # Iterate through attacks
            atkr, dfndr = attack
            if ch.db.positions[atkr.id][dfndr.id] > 1: # if target too far for melee ...
                general_defense[atkr.id] += 1 if simple_check(atkr.dex(), -2) else 0 # ... attemp dodge
                feedback.append("%s is too far to strike %s and tries to dodge!" % (atkr, dfndr)) # ... and let us know
            else:
                remaining_attacks[dbref].append(attack)
    return (feedback, remaining_attacks)

def resolve_moves(ch, moves):
    """
    Resolves all move actions from a single turn.  Does a simple dex check for each character attempting move to see if
    successful, each combantant moves compared and aggregate constructed.

    Args:
        ch (CombatHandler): Combat Handler to update character position.
        mv (List): List of Tuple of actions (String), char (Character), target (Character) of moves to resolve.

    Returns: List of Strings of relative move changes.

    """
    # Calculate results of each move attempt
    results = defaultdict(lambda: defaultdict(int))

    # Iterate over each move attempt.
    for action, char, target in moves:
        i = 1 if action == "rush" else -1 # set distance change based on type of move.
        chng = i if simple_check(char.dex()) else 0 # actual change value if success, 0 if failure
        if chng: # only call if actual value changes
            if ch.adjust_position(char, target, chng):
                chng = 0 # Zero of method call fails as actual change would violate limits. i.e. no actual change.
        keys = sorted([char.id, target.id]) # create a simple index for a deduped list of total changes.
        results[keys[0]][keys[1]] += chng # this ensures same char combinations always added together once

    # Create the feedback strings.
    feedback = []
    directions = ['move closer', 'circle each other', 'move apart', ]
    for cid, mvs in results.iteritems():
        for tid, chng in mvs.iteritems():
            char = ch.db.characters[cid]
            target = ch.db.characters[tid]
            feedback.append("%s and %s %s" % (char, target, directions[chng]))
    return (feedback)