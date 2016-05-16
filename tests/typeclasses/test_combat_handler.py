from evennia.utils.test_resources import EvenniaTest
from evennia import create_script
from typeclasses.characters import Character
from typeclasses.rooms import Room
from mock import Mock

from typeclasses.combat_handler import CombatHandler, MSG_AUTO_TURN_END, MSG_TURN_END
from typeclasses.combat_handler import CombatHandlerExecption

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

        # It should add itself as the combat handler for each character.
        self.assertEqual(ch, c1.ndb.combat_handler)
        self.assertEqual(ch, c2.ndb.combat_handler)

    def test_remove_character(self):
        c1 = self.char1
        c2 = self.char2
        ch = self.ch

        ch.remove_character(c2)
        # It should remove the characeter from all attribute references.
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

    def test_add_action(self):
        c1, c2 = self.ch.db.characters.values()
        ch = self.ch

        # It should add 3 actions for a character
        self.assertTrue(ch.add_action("dodge", c1, None))
        self.assertTrue(ch.add_action("dodge", c1, None))

        # It should fail to add a 4th action
        self.assertFalse(ch.add_action("dodge", c1, None))

        # Char2 actions
        self.assertTrue(ch.add_action("dodge", c2, None))
        self.assertTrue(ch.add_action("dodge", c2, None))

        # It should resolve and reset all actions after everyone enters 3
        for c in [c1, c2]:
            self.assertEqual(0, len(ch.db.actions[c.id]))

    def test_end_turn(self):
        c1, c2 = self.ch.db.characters.values()
        ch = self.ch

        ch.end_turn()
        self.assertIn("{M Next turn begins!  Choose 2 actions ...",
                      (args[0] for name, args, kwargs
                       in c2.msg.mock_calls))


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