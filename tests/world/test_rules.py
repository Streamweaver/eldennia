import random, pprint

from evennia.utils.test_resources import EvenniaTest

from typeclasses.characters import Character
from typeclasses.rooms import Room
from typeclasses.combat_handler import Ranges
from world import rules

class RevolveTestCase(EvenniaTest):
    character_typeclass = Character
    room_typeclass = Room

    def test_revolve_moves(self):
        c1 = self.char1
        c2 = self.char2
        c1.execute_cmd("attack %s" % c2)

        ch = c1.ndb.combat_handler

        moves = []
        for i in range(3):
            mv = random.choice(["rush", "retreat"])
            moves.append((mv, c1, c2))
            mv = random.choice(["rush", "retreat"])
            moves.append((mv, c2, c1))

        changes = rules.resolve_moves(None, moves)
        pp = pprint.PrettyPrinter(indent=3)
        pp.pprint(changes)
        self.assertTrue(changes)
