from evennia.utils.test_resources import EvenniaTest
from evennia import create_script
from typeclasses.characters import Character
from typeclasses.rooms import Room
from mock import Mock

from typeclasses.combat_handler import Distance
from typeclasses.combat_handler import CombatHandler, MSG_AUTO_TURN_END, MSG_TURN_END
from typeclasses.combat_handler import CombatHandlerExecption

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
        self.ch = create_script("combat_handler.CombatHandler")
        self.ch.add_character(self.char1)
        self.ch.add_character(self.char2)

    def test_add_character(self):
        c1, c2 = self.ch.db.characters.values()
        ch = self.ch

        # It should init the base handler properties correctly
        for char in [c1, c2]:
            self.assertTrue(char.id in ch.db.characters)
            self.assertTrue(char.id in ch.db.actions)
            self.assertEquals(len(ch.db.actions[char.id]), 0)
            self.assertEquals(len(ch.db.positions[char.id]), 1)

        # it should have valid positions for each character.
        self.assertTrue(c1.id in ch.db.positions)
        self.assertTrue(c2.id in ch.db.positions[c1.id])
        self.assertTrue(c2.id in ch.db.positions)
        self.assertTrue(c1.id in ch.db.positions[c2.id])

        # It should have same positions for each of the characters.
        self.assertEquals(
            ch.db.positions[c1.id][c2.id],
            ch.db.positions[c2.id][c1.id]
        )

        # It should add itself as the combat handler for each character.
        self.assertEqual(ch, c1.ndb.combat_handler)
        self.assertEqual(ch, c2.ndb.combat_handler)

    def test_remove_character(self):
        c1 = self.char1
        c2 = self.char2
        ch = self.ch

        ch.remove_character(c2)
        # It should remove the characeter from all attribute references.
        self.assertFalse(c2.id in ch.db.positions)
        self.assertFalse(c2.id in ch.db.positions[c1.id])
        self.assertFalse(c2.id in ch.db.characters)
        self.assertFalse(c2.id in ch.db.actions)

        # It should remove the command set from the character
        self.assertFalse(c2.cmdset.has_cmdset('combat_cmdset'))

        # It should message the character they are no longer in combat.
        self.assertIn("You are no longer in combat.",
                      (args[0] for name, args, kwargs
                       in self.char2.msg.mock_calls))

    def test_msg_all(self):
        ch = self.ch
        exp = "This is a test"
        ch.msg_all(exp)
        for char in [self.char1, self.char2]:
            self.assertIn(exp, (args[0] for name, args, kwargs
                                in char.msg.mock_calls))

    def test_adjust_position(self):
        c1, c2 = self.ch.db.characters.values()
        ch = self.ch

        pos1 = ch.db.positions[c1.id][c2.id]

        # Test change to invalid position
        self.assertFalse(ch.adjust_position(c1.id, c2.id, -10))
        self.assertFalse(ch.adjust_position(c1.id, c2.id, 20))

        def _same_pos(pos):
            self.assertEquals(pos, ch.db.positions[c1.id][c2.id])
            self.assertEquals(pos, ch.db.positions[c2.id][c1.id])

        _same_pos(pos1)

        move1 = 1 if pos1 != Distance.Extreme else - 1
        ch.adjust_position(c1.id, c2.id, move1)

        self.assertEquals(pos1 + move1, ch.db.positions[c1.id][c2.id])
        _same_pos(pos1 + move1)

    def test_add_action(self):
        c1, c2 = self.ch.db.characters.values()
        ch = self.ch

        # It should add 3 actions for a character
        self.assertTrue(ch.add_action("rush", c1, c2))
        self.assertTrue(ch.add_action("retreat", c1, c2))
        self.assertTrue(ch.add_action("communicate", c1, c2))

        # It should fail to add a 4th action
        self.assertFalse(ch.add_action("sleep", c1, None))

        # Char2 actions
        self.assertTrue(ch.add_action("shoot", c2, c1))
        self.assertTrue(ch.add_action("shoot", c2, c1))
        self.assertTrue(ch.add_action("shoot", c2, c1))

    def test_end_turn(self):
        c1, c2 = self.ch.db.characters.values()
        ch = self.ch

        ch.end_turn()
        self.assertIn("{M Next turn begins!  Choose 3 actions ...",
                      (args[0] for name, args, kwargs
                       in c2.msg.mock_calls))

    def test_msg_positions(self):
        c1, c2 = self.ch.db.characters.values()
        ch = self.ch

        ch.msg_positions(c1)
        exp = "Target(Range): %s(%s)" % (c2,
                                          Distance(ch.db.positions[c1.id][c2.id]).name)
        self.assertIn(exp, (args[0] for name, args, kwargs
                       in c1.msg.mock_calls))

    def test_at_repeat(self):
        c1, c2 = self.ch.db.characters.values()
        ch = self.ch

        # It should not automatically message everyone
        ch.at_repeat("endturn")
        self.assertNotIn(MSG_AUTO_TURN_END, (args[0] for name, args, kwargs
                                             in c1.msg.mock_calls))

        # It should message everyone turn ending automatically
        ch.at_repeat()
        self.assertIn(MSG_AUTO_TURN_END, (args[0] for name, args, kwargs
                                          in c1.msg.mock_calls))

    def test_end_turn(self):
        c1, c2 = self.ch.db.characters.values()
        ch = self.ch

        # Add some actions
        ch.add_action("shoot", c1, c2)
        ch.add_action("rush", c2, c1)
        ch.add_action("aim", c1, None)

        ch.end_turn()
        # It should let everyone know the turn ends
        for c in [c1, c2]:
            self.assertIn(MSG_TURN_END, (args[0] for name, args, kwargs
                                              in c.msg.mock_calls))
        # It should have reset actions for everyone.
        for c in [c1, c2]:
            self.assertEqual(0, len(ch.db.actions[c.id]))

        # It should end combat and notify the last character if only one left.
        ch.remove_character(c1)
        ch.end_turn()
        self.assertIn("Combat has ended.", (args[0] for name, args, kwargs
                                         in c2.msg.mock_calls))

    def test_set_distance(self):
        c1, c2 = self.ch.db.characters.values()
        ch = self.ch

        # It should set new valid positions.
        ch.set_distance(6, 0)
        self.assertEqual(6, ch.db.distance_max)
        self.assertEqual(0, ch.db.distance_min)

        # It should not allow setting of invalid distances
        self.assertRaises(CombatHandlerExecption, ch.set_distance, 7, 0)
        self.assertRaises(CombatHandlerExecption, ch.set_distance, 6, -1)
        self.assertRaises(CombatHandlerExecption, ch.set_distance, 0, 6)

        # It should reset distance on new max value
        for i in range(8): # Move them to max
            ch.adjust_position(c1.id, c2.id, 1)
        ch.set_distance(5, 0)
        self.assertEqual(5, ch.get_distance(c1.id, c2.id))

    def test_get_distance(self):
        c1, c2 = self.ch.db.characters.values()
        ch = self.ch

        exp = ch.db.positions[c1.id][c2.id]
        self.assertEqual(exp, ch.get_distance(c1.id, c2.id))