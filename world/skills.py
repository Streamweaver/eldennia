"""
Handles skills in the game.  Must of this adapted from avinneve.worlds.skills
"""

from ainneve.world.skills import Skill, SkillException

_SKILL_DATA = {
    # AGILITY SKILLS
    "dodge": {
        "name": "Dodge",
        "base": "AGL",
        "desc": "Skill at ducking and avoiding attacks."
    },
    "rifles": {
        "name": "Rifles",
        "base": "AGL",
        "desc": "Skill at shooting all kind of rifles."
    },
    "melee": {
        "name": "Melee",
        "base": "AGL",
        "desc": "Skill with melee weapons"
    },
    "heavy weapons": {
        "name": "Heavy Weapons",
        "base": "AGL",
        "desc": "Skill at using missile launchers and crewed weapons."
    },
    "sleight of hand": {
        "name": "Sleight of Hand",
        "base": "AGL",
        "desc": "Skill at picking pockets and physical misdirection."
    },
    "throwing": {
        "name": "Throwing",
        "base": "AGL",
        "desc": "Skill at throwing weapons and grenades."
    },
    # STRENGTH
    "armor": {
        "name": "Armor",
        "base": "STR",
        "desc": "Skill at wearing non-powered armors."
    },
    "brawling": {
        "name": "Brawling",
        "base": "STR",
        "desc": "Skill in hand to hand combat."
    },
    # KNWLEGE SKILLS
    "astrography": {
        "name": "Astrography",
        "base": "KNW",
        "desc": "Skill in stellar mapping and plotting jumps."
    },
    "bureaucracy": {
        "name": "Bureaucracy",
        "base": "KNW",
        "desc": "Skill in manipulating or examining records, official requests."
    },
    "business": {
        "name": "Business",
        "base": "KNW",
        "desc": "Skill at trading, negotiating business deals and finding profit."
    },
    "cultures": {
        "name": "Cultures",
        "base": "KNW",
        "desc": "Understanding of cultures and diplomacy to avoid conflict."
    },
    "intimidation": {
        "name": "Intimidation",
        "base": "KNW",
        "desc": "Skill at getting others to back down or force them to obey."
    },
    "languages": {
        "name": "Languages",
        "base": "KNW",
        "desc": "Skill at understanding and deciphering languages"
    },
    "scholar": {
        "name": "Scholar",
        "base": "KNW",
        "desc": "Skill at examining artifacts or scientific samples."
    },
    "streetwise": {
        "name": "Streetwise",
        "base": "KNW",
        "desc": "Skill at underworld negotiations, uncovering rumors and finding the black market."
    },
    "survival": {
        "name": "Survival",
        "base": "KNW",
        "desc": "Skill at enduring and avoiding damage in hostile environments."
    },
    # MCHANICAL SKILLS
    "powered armor": {
        "name": "Powered Armor",
        "base": "MCH",
        "desc": "Skill at operating powered armor and exoskeletons."
    },
    "gunnery": {
        "name": "Gunnery",
        "base": "MCH",
        "desc": "Skill operating vehicle mounted weapons."
    },
    "navigation": {
        "name": "Navigation",
        "base": "MCH",
        "desc": "Skill at plotting courses."
    },
    "piloting": {
        "name":  "piloting",
        "base": "MCH",
        "desc": "Skill at operating starships and atmospheric vehicles."
    },
    "sensors":  {
        "name": "Sensors",
        "base": "MCH",
        "desc":  "Skill operating starship or vehicle sensors and cloaks."
    },
    "shields": {
        "name": "Shields",
        "base": "MCH",
        "desc": "Skill at operating shields."
    },
    # PERCEPTION SKILLS
    "bargain": {
        "name": "Bargain",
        "base": "PER",
        "desc": "Skill at negotiting prices when buying and selling."
    },
    "gambling": {
        "name": "Gambling",
        "base": "PER",
        "desc": "Skill at games of chance and high stakes games."
    },
    "stealth": {
        "name": "Stealth",
        "base": "PER",
        "desc": "Skill at hiding or moving while remaining undetected."
    },
    "investigation": {
        "name":  "Investigation",
        "base": "PER",
        "desc": "Skill at examining evidence to gain bonuses or information."
    },
    "persuasion": {
        "name": "Persuasion",
        "base": "PER",
        "desc": "Skill at convincing others."
    },
    "search": {
        "name": "Search",
        "base": "PER",
        "desc": "Skill at examining areas for hidden items."
    },
    # TCHNICAL SKILLS
    "armorer": {
        "name": "Armorer",
        "base": "TCH",
        "desc": "Skill at repairing, improving or salvaging armor."
    },
    "computers": {
        "name": "Computers",
        "base": "TCH",
        "desc": "Skill at operating, and hacking computers."
    },
    "demolitions": {
        "name": "Demolitions",
        "base": "TCH",
        "desc": "Skill setting or disarming explosives."
    },
    "power armor tech": {
        "name": "Power Armor tech",
        "base": "TCH",
        "desc": "Skill at repairing, improving or salvaging power armor."
    },
    "gunsmith": {
        "name": "gunsmith",
        "base": "TCH",
        "desc": "Skill at repairing, improving or salvaging firearms."
    },
    "starship engineering": {
        "name": "Starship Engineering",
        "base": "TCH",
        "desc": "Skill at repairing, improving or salvaging starships."
    },
    "gunnary tech": {
        "name": "Gunnary tech",
        "base": "TCH",
        "desc": "Skill at repairing, improving or salvaging vehicle mounted weapons."
    },
    "medicine": {
        "name": "Medicine",
        "base": "TCH",
        "desc": "Skill at healing and operating medical devices and scanners."
    },
    "robotics": {
        "name": "Robotics",
        "base": "TCH",
        "desc": "Skill at repairing, improving or salvaing robotics and cybernetics. "
    },
    "security": {
        "name": "Security",
        "base": "TCH",
        "desc": "Skill at breaching security systems and locks."
    }
}

SKILL_LIST = [s.lower() for s in _SKILL_DATA.keys()]
STR_SKILLS = [s["name"].lower() for s in _SKILL_DATA.values() if s['base'] == 'STR']
AGL_SKILLS = [s["name"].lower() for s in _SKILL_DATA.values() if s['base'] == 'AGL']
KNW_SKILLS = [s["name"].lower() for s in _SKILL_DATA.values() if s['base'] == 'KNW']
MCH_SKILLS = [s["name"].lower() for s in _SKILL_DATA.values() if s['base'] == 'MCH']
PER_SKILLS = [s["name"].lower() for s in _SKILL_DATA.values() if s['base'] == 'PER']
TCH_SKILLS = [s["name"].lower() for s in _SKILL_DATA.values() if s['base'] == 'TCH']

def load_skill(skill):
    """Retrieves an instance of a `Skill` class.

    Args:
        skill (str): case insensitive skill name

    Returns:
        (Skill): instance of the named Skill
    """
    skill = skill.lower()
    if skill in SKILL_LIST:
        return Skill(**_SKILL_DATA[skill])
    else:
        raise SkillException('Invalid skill name.')