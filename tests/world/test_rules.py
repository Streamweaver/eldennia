import random, pprint

from collections import defaultdict

from evennia.utils.test_resources import EvenniaTest

from typeclasses.characters import Character
from typeclasses.rooms import Room
from typeclasses.combat_handler import Distance
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

        results = rules.resolve_moves(ch, moves)
        self.assertEqual(len(results), 1)

    def test_resolve_melee_to_dodge(self):
        c1 = self.char1
        c2 = self.char2
        c1.execute_cmd("attack %s" % c2)
        ch = c1.ndb.combat_handler

        attacks = defaultdict(list)
        general_defense = defaultdict(int)

        pos = 6 - ch.db.positions[c1.id][c2.id]
        ch.adjust_position(c1, c2, pos) # Make them far apart

        for i in range(3):
            attacks[c1.id].append((c1, c2))
            attacks[c2.id].append((c2, c1))
        fb, atks = rules.melee_to_dodge(ch, attacks, general_defense)
        exp = 6 - len(atks[c1.id]) + len(atks[c2.id])
        self.assertEquals(len(fb), exp)
