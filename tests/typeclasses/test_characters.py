from random import randint
from evennia.utils.test_resources import EvenniaTest
from evennia.contrib.dice import roll_dice

from typeclasses.characters import Character
from typeclasses.rooms import Room

class CharacterTestCase(EvenniaTest):
    character_typeclass = Character
    room_typeclass = Room

    def test_str(self):
        self.assertTrue(self.char1.db.str, self.char1.str())
        self.char1.db.wounds["str"] = self.char1.db.str
        self.assertEquals(0, self.char1.str())
        self.char1.db.wounds["str"] = 100
        self.assertEquals(0, self.char1.str())

    def test_dex(self):
        self.assertTrue(self.char1.db.dex, self.char1.dex())
        self.char1.db.wounds["dex"] = self.char1.db.dex
        self.assertEquals(0, self.char1.dex())
        self.char1.db.wounds["dex"] = 100
        self.assertEquals(0, self.char1.dex())

    def test_end(self):
        self.assertTrue(self.char1.db.end, self.char1.end())
        self.char1.db.wounds["end"] = self.char1.db.end
        self.assertEquals(0, self.char1.end())
        self.char1.db.wounds["end"] = 100
        self.assertEquals(0, self.char1.end())

    def test_wounds(self):
        self.assertEqual(0, self.char1.wounds())
        for atrb in ["dex", "str", "end"]:
            self.char1.db.wounds[atrb] = 1
        actual = sum(self.char1.db.wounds.values())
        self.assertEqual(3, actual)

    def test_health(self):
        self.assertEqual(self.char1.health(),
                         sum([self.char1.db.end, self.char1.db.str, self.char1.db.dex]))

    def test_is_incapacitated(self):
        self.assertFalse(self.char1.is_incapacitated())
        self.char1.add_damage(100)
        self.assertTrue(self.char1.is_incapacitated())

    def test_add_damage(self):
        # self.char1.add_damage(self.char1.db.end)
        # self.assertEquals(self.char1.db.wounds["end"], self.char1.db.end)
        for _ in range(10):
            self.char1.add_damage(
                randint(
                    1,
                    roll_dice(2, 6)
                ))
            self.assertTrue(self.char1.wounds() > 0)
            if self.char1.db.wounds["end"] < self.char1.db.end:
                self.assertEquals(0, self.char1.db.wounds["dex"])
                self.assertEquals(0, self.char1.db.wounds["str"])
            if self.char1.db.wounds["dex"] > 0:
                self.assertEqual(0, self.char1.end())
            if self.char1.db.wounds["str"] > 0:
                self.assertEqual(0, self.char1.end())
