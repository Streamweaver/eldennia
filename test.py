"""
This is just a file scratchpad to play with outcome examples for when I'm tired and can't remember.
"""
# from evennia.contrib.dice import roll_dice
import random

def run_outer():
    tdict = {
        1: "outer",
    }
    tlist = ["outer"]
    run_inner(tdict, tlist)
    return (tdict, tlist)

def run_inner(tdict, tlist):
    tdict[1] = "inner"
    tdict[2] = "inner"
    tlist.append("inner")

def move_compare():
    actions = ["rush", "retreat", "shoot"]
    for _ in range(20):
        action = random.choice(actions)
        i = 1 if action == "rush" else -1 if action == "retreat" else 0
        print("%s" % i)

def ordered_dict():
    data = {
        6: {
            "initiative": 9,
            "dex": 8,
            "melee": (1, 2),
            "ranged": (1, 2)
        },
        7: {
            "initiative": 11,
            "dex": 6,
            "melee": (1, 2),
            "ranged": (1, 2)
        },
        8: {
            "initiative": 9,
            "dex": 7,
            "melee": (1, 2),
            "ranged": (1, 2)
        },
    }
    flattened = data.items()
    random.shuffle(flattened)
    print(sorted(flattened, key=lambda x: (x[1]["initiative"], x[1]["dex"]), reverse=True))

def idx_iteritems():
    data = {i: i+1 for i in range(10)}
    for idx, item in enumerate(data.iteritems()):
        print(idx, item)

if __name__ == "__main__":
    idx_iteritems()