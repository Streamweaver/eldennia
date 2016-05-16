from collections import defaultdict, OrderedDict
from random import shuffle

from evennia.contrib.dice import roll_dice

from world.rules.rollers import simple_check
from commands.combat import CmdDodge, CmdParry, CmdAim, CmdRush, CmdShoot, CmdStrike
from world.rules.rollers import roll_attribute, get_mod, get_effect

def resolve_combat_turn(combat_handler):
    """
    Resolves the outcome of actions in a single combat round.
    Args:
        combat_handler: instance of combat_handler

    """
    ch = combat_handler
    feedback = {} # {"actionname": ["string", "string", ...], ... }

    # {dbref: {"init": int, "melee": [(atker, tgt), ...], "ranged": [(atkr, tgt), ...]},...}
    attacks = _init_attacks(c for c in ch.db.characters.values())
    mods = _init_modifiers(c for c in ch.db.characters.values())

    # Iterate over character action queues and sort by resolution.
    for dbref, queue in ch.db.actions.iteritems():
        for item in queue:
            action, char, target = item
            if action == CmdRush.key:
                attacks[dbref]["init"] += 2
                mods[dbref]["general"]["penalty"] += 1
            if action == CmdAim.key: # Add automatic ranged bonuses
                mods[dbref]["ranged"]["bonus"] += 1
            if action == CmdParry.key:# Add automatic Melee defense
                mods[dbref]["melee"]["defense"] += max([get_mod(char.dex()), get_mod(char.str())]) # TODO change to skill
                mods[dbref]["general"]["penalty"] += 1
            if action == CmdShoot.key: # Queue a ranged attack
                attacks[dbref]["ranged"].append((char, target))
            if action == CmdStrike.key: # Queue melee attack
                attacks[dbref]["melee"].append((char, target))
            if action == CmdDodge.key: # Add a general defense if dex check
                mods[dbref]["general"]["defense"] += 1
                mods[dbref]["general"]["penalty"] += 1

    ordered_attacks = sort_attacks(attacks)
    round = 0
    for attacks in ordered_attacks.values():
        # First ranged attacks
        ranged = attacks["ranged"][round] if len(attacks["ranged"]) > round else None
        if ranged:
            resolve_ranged_attack(ranged[0], ranged[1], mods)
        # ... then melee
        melee = attacks["melee"][round] if len(attacks["melee"]) > round else None
        if melee:
            resolve_melee_attack(melee[0], melee[1], mods)
        round += 1
        if round == 2: # At most there can only be 2 attacks.
            break

    return feedback

def sort_attacks(attacks):
    """
    Creates attack order sorted by initiative score, then dex and random if still tied.
    Args:
        attacks:

    Returns: OrderedDict based on initiative

    """
    data = attacks.items()
    shuffle(data) # This step creates random selction in case of init and dex tied
    return OrderedDict(sorted(data, key=lambda x: (x[1]["init"], x[1]["dex"]), reverse=True))

def _init_attacks(characters):
    """
    Initiates attack data for each character and returns the dict.
    Args:
        characters: List of Character objects to initialize data for.

    Returns: dict format {dbref: {"init": int, "melee": [], "ranged": [], ...]},...}

    """
    attacks = {}
    for character in characters:
        attacks[character.id] = {
            "init": roll_attribute(character.dex()),
            "dex": character.dex(),
            "melee": [],
            "ranged": []
        }
    return attacks

def _init_modifiers(characters):
    """
    Initiates attack modifier data for each character and returns the dict.
    Args:
        characters: List of Character objects to initialize data for.

    Returns: dict format {dbref: {"melee": "penalty": 0, "bonus": 0, "defense": 0}

    """
    mods = {}
    base = {"bonus": 0, "penalty": 0, "defense": 0}
    for c in characters:
        mods[c.id] = {
            "general": base.copy(),
            "melee": base.copy(),
            "ranged": base.copy()
        }
    return mods

def resolve_ranged_attack(attacker, target, mods):
    # 2d6 + skill + ability mod + attacker ranged bonus + attacker general bonus - target ranged defense - target general defense
    result = sum([
        roll_attribute(attacker.dex()), # 2d6 + attacker ability mod
        0, # Skill will go here
        mods[attacker.id]["ranged"]["bonus"],
        mods[attacker.id]["general"]["bonus"],
        - mods[attacker.id]["ranged"]["penalty"],
        - mods[attacker.id]["general"]["penalty"],
        - mods[target.id]["ranged"]["defense"],
        - mods[target.id]["general"]["defense"]
    ])
    if result > 7:
        effect = get_effect(result)
        dmg = roll_dice(1, 6) + effect
        target.add_damage(roll_dice(1, 6) + effect)
        target.msg("%s shoots you for %i damage!" % (attacker, dmg))
        attacker.msg("You shoot %s for %i damage!" % (target, dmg))
    else:
        target.msg("%s fires at you and misses!" % attacker)
        attacker.msg("You fire at %s and miss!" % target)

def resolve_melee_attack(attacker, target, mods):
    result = sum([
        roll_attribute(attacker.dex()), # 2d6 + attacker ability mod
        0, # Skill will go here
        mods[attacker.id]["melee"]["bonus"],
        mods[attacker.id]["general"]["bonus"],
        - mods[attacker.id]["melee"]["penalty"],
        - mods[attacker.id]["general"]["penalty"],
        - mods[target.id]["melee"]["defense"],
        - mods[target.id]["general"]["defense"]
    ])
    if result > 7:
        effect = get_effect(result)
        dmg = roll_dice(1, 6) + effect
        target.add_damage(roll_dice(1, 6) + effect)
        target.msg("%s punches you for %i damage!" % (attacker, dmg))
        attacker.msg("You punch %s for %i damage!" % (target, dmg))
    else:
        target.msg("%s punches at you and misses!" % attacker)
        attacker.msg("You punch at %s and miss!" % target)

