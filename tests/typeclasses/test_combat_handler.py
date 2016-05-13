from evennia.utils.test_resources import EvenniaTest
from typeclasses.characters import Character
from typeclasses.rooms import Room
from mock import Mock
from typeclasses.combat_handler import Distance

class DistanceTestCase(EvenniaTest):
    def test_basic(self):
        self.assertEqual(Distance(1), 1)
        self.assertEqual(Distance(1).name, "Close")

class CombatHandlerTestCase(EvenniaTest):
    character_typeclass = Character
    room_typeclass = Room

    def setUp(self):
        super(CombatHandlerTestCase, self).setUp()
        self.char1.msg = Mock()
        self.char2.msg = Mock()

    def test_add_character(self):
        c1 = self.char1
        c2 = self.char2
        c1.execute_cmd('attack %s' % c2)

        # Test that characters get the same ch
        self.assertTrue(c1.ndb.combat_handler is c2.ndb.combat_handler)

        # Test attributes set properly
        ch = c1.ndb.combat_handler
        for char in [c1, c2]:
            self.assertTrue(char.id in ch.db.characters)
            self.assertTrue(char.id in ch.db.turn_actions)
            self.assertEquals(len(ch.db.turn_actions[char.id]), 0)
            self.assertEquals(len(ch.db.positions[char.id]), 1)

        # Test positions set correctly.
        self.assertTrue(c1.id in ch.db.positions)
        self.assertTrue(c2.id in ch.db.positions[c1.id])
        self.assertTrue(c2.id in ch.db.positions)
        self.assertTrue(c1.id in ch.db.positions[c2.id])

        self.assertEquals(
            ch.db.positions[c1.id][c2.id],
            ch.db.positions[c2.id][c1.id]
        )

    def test_remove_character(self):
        c1 = self.char1
        c2 = self.char2
        c1.execute_cmd('attack %s' % c2)

        ch = c1.ndb.combat_handler
        ch.remove_character(c2)
        self.assertFalse(c2.id in ch.db.positions)
        self.assertFalse(c2.id in ch.db.positions[c1.id])
        self.assertFalse(c2.id in ch.db.characters)
        self.assertFalse(c2.id in ch.db.turn_actions)
        # make sure commandset removed
        self.assertFalse(c2.cmdset.has_cmdset('combat_cmdset'))
        # check msg
        self.assertIn("You are no longer in combat.",
                      (args[0] for name, args, kwargs
                       in self.char2.msg.mock_calls))

    def test_msg_all(self):
        self.char1.execute_cmd('attack %s' % self.char2)
        ch = self.char2.ndb.combat_handler
        exp = "This is a test"
        ch.msg_all(exp)
        for char in [self.char1, self.char2]:
            self.assertIn(exp, (args[0] for name, args, kwargs
                       in char.msg.mock_calls))

    def test_adjust_position(self):
        c1 = self.char1
        c2 = self.char2
        c2.execute_cmd('attack %s' % c1)
        ch = c2.ndb.combat_handler

        pos1 = ch.db.positions[c1.id][c2.id]

        # Test change to invalid position
        self.assertFalse(ch.adjust_position(c1, c2, -10))
        self.assertFalse(ch.adjust_position(c1, c2, 20))

        def _same_pos(pos):
            self.assertEquals(pos, ch.db.positions[c1.id][c2.id])
            self.assertEquals(pos, ch.db.positions[c2.id][c1.id])

        _same_pos(pos1)

        move1 = 1 if pos1 != Distance.Extreme else - 1
        ch.adjust_position(c1, c2, move1)

        self.assertEquals(pos1 + move1, ch.db.positions[c1.id][c2.id])
        _same_pos(pos1 + move1)

    def test_add_action(self):
        c1 = self.char1
        c2 = self.char2
        c1.execute_cmd('attack %s' % c2)
        ch = c2.ndb.combat_handler

        # Char1 actions
        self.assertTrue(ch.add_action("rush", c1, c2))
        self.assertTrue(ch.add_action("retreat", c1, c2))
        self.assertTrue(ch.add_action("communicate", c1, c2))
        self.assertFalse(ch.add_action("sleep", c1, c2))

        # Char2 actions
        self.assertTrue(ch.add_action("shoot", c2, c1))
        self.assertTrue(ch.add_action("shoot", c2, c1))
        self.assertTrue(ch.add_action("shoot", c2, c1))

    def test_end_turn(self):
        c1 = self.char1
        c2 = self.char2
        c1.execute_cmd("attack %s" % c2)
        ch = c1.ndb.combat_handler

        ch.end_turn()
        self.assertIn("{M Next turn begins!  Choose 3 actions ...",
                      (args[0] for name, args, kwargs
                       in c2.msg.mock_calls))

    # def test_msg_positions(self):
    #     c1 = self.char1
    #     c2 = self.char2
    #     c1.execute_cmd("attack %s" % c2)
    #     ch = c1.ndb.combat_handler
    #
    #     ch.msg_positions(c1)
    #     exp = "Targets(Range): %s(%s)" % (c2,
    #                                       Distance(ch.db.positions[c1.id][c2.id]).name)
    #     self.assertIn(exp, (args[0] for name, args, kwargs
    #                    in c1.msg.mock_calls))