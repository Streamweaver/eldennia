from mock import Mock

from evennia.utils.test_resources import EvenniaTest
from evennia import create_script

from commands.combat import CmdRush, CmdStrike, CmdRetreat, CmdBlock, CmdShoot, CmdAim, CmdCover, CmdDodge, CmdAttack
from world.rules.resolvers import resolve_combat_turn
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
        resolve_combat_turn(self.ch)
        for c in [c1, c2]:
            actual = list(args[0] for name, args, kwargs in c2.msg.mock_calls)
            self.assertIn("You dodge.", actual)
