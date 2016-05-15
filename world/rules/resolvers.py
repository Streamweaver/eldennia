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
    general_defense = defaultdict(int) # {dbref: 0, ... }
    ranged_defense = defaultdict(int)
    ranged_bonus = defaultdict(int)
    melee_defense = defaultdict(int)
    melee_bonus = defaultdict(int)
    ranged_attacks = defaultdict(list)
    melee_attacks = defaultdict(list)
    moves = [] # [("rush", character, traget), ...]
    feedback = {} # {"actionname": ["string", "string", ...], ... }

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

    feedback["moves"]= resolve_moves(ch, moves)
    feedback['dodge'] = melee_to_dodge(ch, melee_attacks, general_defense)
    return feedback

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
        for idx, attack in enumerate(attacks): # Iterate through attacks
            attacker, target = attack
            if ch.get_distance(attacker.id, target.id) > 1: # if target too far for melee ...
                general_defense[attacker.id] += 1 if simple_check(attacker.dex(), -2) else 0 # dodge instead ...
                attacks.pop(idx)
                feedback.append("%s can't reach %s and dodges!" % (attacker, target)) # ... and let us know
        melee_attacks[dbref] = [attack for attack in attacks if ch.get_distance(attack[0].id, attack[1].id) <= 1]
    return list(set(feedback))

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
        i = 1 if action == CmdRush.key else -1 # set distance change based on type of move.
        chng = i if simple_check(char.dex()) else 0 # actual change value if success, 0 if failure
        if chng: # only call if actual value changes
            if ch.adjust_position(char.id, target.id, chng):
                chng = 0 # Zero if method call fails as actual change would violate limits. i.e. no actual change.
        keys = sorted([char.id, target.id]) # create a simple index for a deduped list of total changes.
        results[keys[0]][keys[1]] += chng # this ensures same char combinations always added together once

    # Create the feedback strings.
    feedback = []
    directions = ['move closer', 'circle each other', 'move apart', ]
    for cid, mvs in results.iteritems():
        for tid, chng in mvs.iteritems():
            char = ch.db.characters[cid]
            target = ch.db.characters[tid]
            feedback.append("%s and %s %s." % (char, target, directions[chng]))
    return feedback