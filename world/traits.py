"""
Local implentation of ainneve.world.traits
"""
from ainneve.world.traits import Trait, TraitException

TRAIT_DATA = {
    "agl": {
        "name": "Agility",
        "base": 2,
        "desc": "Measure of speed, nimbleness and dexterity"
    },
    "str": {
        "name": "Strength",
        "base": 2,
        "desc": "Physical power, conditioning and toughness."
    },
    "knw": {
        "name": "Knowledge",
        "base": 2,
        "desc": "General intelligence, education and training."
    },
    "mch": {
        "name": "Mechanical",
        "base": 2,
        "desc": "Aptitude with operating equiptment and machinery."
    },
    "per": {
        "name": "Perception",
        "base": 2,
        "desc": "Measure of awareness, emotinal intelligence and mental sharpness."
    },
    "tch": {
        "name": "Technical",
        "base": 2,
        "desc": "High tech and engineering aptitude."
    }
}
TRAIT_ORDER = ("AGL", "STR", "KNW", "MCH", "PER", "TCH")

def format_trait(trait):
    d = trait.actual/3
    m = trait.actual%3
    return "%iD" % d if m == 0 else "%iD+%i" % (d, m)