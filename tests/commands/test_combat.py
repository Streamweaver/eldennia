from evennia.commands.default.tests import CommandTest
from evennia.utils import create

from typeclasses.characters import Character
from commands import combat

class CmdAttackTestCase(CommandTest):
    character_typeclass = Character

    def setUp(self):
        super(CmdAttackTestCase, self).setUp()

        # Create character 3 and 4
        self.player3 = create.create_player("TestPlayer3", email="test3@test.com",
                                  password="testpassword",
                                  typeclass=self.player_typeclass)
        self.char3 = create.create_object(self.character_typeclass, key="Char3",
                                  location=self.room1, home=self.room1)
        self.char3.player = self.player3

        self.player4 = create.create_player("TestPlayer4", email="test4@test.com",
                                            password="testpassword",
                                            typeclass=self.player_typeclass)
        self.char4 = create.create_object(self.character_typeclass, key="Char4",
                                          location=self.room1, home=self.room1)
        self.char4.player = self.player4

    def test_cmd(self):
        "Basic function test cases"
        c1 = self.char1 # caller by default
        c2 = self.char2
        c3 = self.char3
        c4 = self.char4

        # Should not work on unfound target & creates no ch
        self.call(combat.CmdAttack(), "NoTarget", "Could not find 'NoTarget'.")
        self.assertIsNone(c1.ndb.combat_handler)

        # Test successful initiate attack
        self.call(combat.CmdAttack(), "%s" % c2, "You attack %s! You are in combat." % c2)
        self.assertEqual(c1.ndb.combat_handler, c2.ndb.combat_handler)

        # Should not work if attacker or target in combat
        self.call(combat.CmdAttack(), "%s" % c2, "Finish this fight before the next.")

        # If a seperate fight should not work.
        self.call(combat.CmdAttack(), "%s" % c4, "You attack %s! You are in combat."
                  % c4, caller=c3)
        # Should fail if trying to join other combat
        self.call(combat.CmdAttack(), "%s" % c3, "Finish this fight before the next.")

class CmdRushTestCase(CommandTest):
    character_typeclass = Character

    def test_cmd(self):
        c1 = self.char1
        c2 = self.char2
        c1.execute_cmd("attack %s" % c2)

        for i in range(3):
            self.call(combat.CmdRush(), "%s" % c2, "You try to move closer to %s." % c2)
        self.call(combat.CmdRush(), "%s" % c2, "You can only queue 3 actions in a turn.")

class CmdRetreatTestCase(CommandTest):
    character_typeclass = Character

    def test_cmd(self):
        c1 = self.char1
        c2 = self.char2
        c1.execute_cmd("attack %s" % c2)

        for i in range(3):
            self.call(combat.CmdRetreat(), "%s" % c2, "You try to move away from %s." % c2)
        self.call(combat.CmdRetreat(), "%s" % c2, "You can only queue 3 actions in a turn.")

class CmdDodgeTestCase(CommandTest):
    character_typeclass = Character

    def test_cmd(self):
        c1 = self.char1
        c2 = self.char2
        c1.execute_cmd("attack %s" % c2)

        for i in range(3):
            self.call(combat.CmdDodge(), "", "You try to dodge all attacks.")
        self.call(combat.CmdDodge(), "%s" % c2, "You can only queue 3 actions in a turn.")

class CmdCoverTestCase(CommandTest):
    character_typeclass = Character

    def test_cmd(self):
        c1 = self.char1
        c2 = self.char2
        c1.execute_cmd("attack %s" % c2)

        for i in range(3):
            self.call(combat.CmdCover(), "", "You duck behind cover.")
        self.call(combat.CmdCover(), "%s" % c2, "You can only queue 3 actions in a turn.")

class CmdBlockTestCase(CommandTest):
    character_typeclass = Character

    def test_cmd(self):
        c1 = self.char1
        c2 = self.char2
        c1.execute_cmd("attack %s" % c2)

        for i in range(3):
            self.call(combat.CmdBlock(), "", "You block incoming attacks.")
        self.call(combat.CmdBlock(), "%s" % c2, "You can only queue 3 actions in a turn.")

class CmdAimTestCase(CommandTest):
    character_typeclass = Character

    def test_cmd(self):
        c1 = self.char1
        c2 = self.char2
        c1.execute_cmd("attack %s" % c2)

        for i in range(3):
            self.call(combat.CmdAim(), "", "You take time to aim.")
        self.call(combat.CmdAim(), "%s" % c2, "You can only queue 3 actions in a turn.")
