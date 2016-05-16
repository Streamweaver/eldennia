from mock import Mock
from collections import defaultdict

from evennia.utils.test_resources import EvenniaTest
from evennia import create_script

from commands.combat import CmdRush, CmdStrike, CmdParry, CmdShoot, CmdAim, CmdDodge, CmdAttack
from world.rules.resolvers import resolve_combat_turn, sort_attacks
from typeclasses.characters import Character
from typeclasses.rooms import Room

class ResolversTestCase(EvenniaTest):
    character_typeclass = Character
    room_typeclass = Room

    def setUp(self):
        super(ResolversTestCase, self).setUp()
        self.char1.msg = Mock()
        self.char2.msg = Mock()
        self.ch = create_script("combat_handler.CombatHandler")
        self.ch.end_turn = Mock()  # Mock this so it doesn't call resolve_combat_turn on it's own.
        self.ch.add_character(self.char1)
        self.ch.add_character(self.char2)

    # def test_resolve_combat_turn(self):
    #     c1 = self.char1
    #     c2 = self.char2
    #     for c in [c1, c2]:
    #         self.ch.add_action(CmdDodge.key, c, None)
    #     fb = resolve_combat_turn(self.ch)
    #     self.assertTrue(fb)

    def test_order_attacks(self):
        data = {
            6: {
                "init": 9,
                "dex": 8,
                "melee": (1, 2),
                "ranged": (1, 2)
            },
            7: {
                "init": 11,
                "dex": 6,
                "melee": (1, 2),
                "ranged": (1, 2)
            },
            8: {
                "init": 9,
                "dex": 7,
                "melee": (1, 2),
                "ranged": (1, 2)
            },
            9: {
                "init": 3,
                "dex": 6,
                "melee": (1, 2),
                "ranged": (1, 2)
            },
            10: {
                "init": 9,
                "dex": 7,
                "melee": (1, 2),
                "ranged": (1, 2)
            },
        }
        attacks = sort_attacks(data)
        exp = attacks.keys()
        self.assertEqual(exp.index(6), 1)
        self.assertEqual(exp.index(7), 0)
        self.assertIn(exp.index(8), [2, 3])
        self.assertEqual(exp.index(9), 4)
        self.assertIn(exp.index(10), [2, 3])