from mock import Mock
from collections import defaultdict

from evennia.utils.test_resources import EvenniaTest
from evennia import create_script

from commands.combat import CmdRush, CmdStrike, CmdRetreat, CmdBlock, CmdShoot, CmdAim, CmdCover, CmdDodge, CmdAttack
from world.rules.resolvers import resolve_combat_turn, melee_to_dodge, resolve_moves
from typeclasses.combat_handler import Distance
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

    def test_resolve_combat_turn(self):
        c1 = self.char1
        c2 = self.char2
        for c in [c1, c2]:
            self.ch.add_action(CmdDodge.key, c, None)
        fb = resolve_combat_turn(self.ch)
        self.assertTrue(fb)

    def test_melee_to_dodge(self):
        c1 = self.char1
        c2 = self.char2
        while (self.ch.get_distance(c1.id, c2.id) < Distance.Extreme):
            extreme = self.ch.adjust_position(c1.id, c2.id, 1)

        melee = {
            c1.id: [(c1, c2) for i in range(3)],
            c2.id: [(c2, c1) for i in range(3)]
        }
        defense = defaultdict(int)
        fb = melee_to_dodge(self.ch, melee, defense)
        self.assertEquals(0, len(melee[c1.id]))
        self.assertEquals(0, len(melee[c2.id]))
        self.assertIn(defense[c1.id], range(0,4))
        self.assertIn(defense[c2.id], range(0, 4))

    def test_resolve_moves(self):
        moves = []
        for _  in range(4):
            self.ch.add_action(CmdRush.key, self.char1, self.char2)
            self.ch.add_action(CmdRetreat.key, self.char2, self.char1)
            moves.append((CmdRush.key, self.char1, self.char2))
            moves.append((CmdRetreat.key, self.char2, self.char1))

        fb = resolve_moves(self.ch, moves)
        self.assertEquals(1, len(fb))