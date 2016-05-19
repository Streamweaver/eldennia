from evennia.utils.test_resources import EvenniaTest

from ainneve.world.traits import Trait

from typeclasses.characters import Character
from world.traits import TRAIT_DATA, format_trait

class TraitsTestCase(EvenniaTest):
    character_typeclass = Character

    def setUp(self):
        super(TraitsTestCase, self).setUp()

    def test_add(self):
        "Not really a unit test so much as me confirming this is how the add works."
        for k, v in TRAIT_DATA.iteritems():
            self.char1.traits.add(k, v["name"], base=v["base"], type="static")
        print(self.char1.traits.get('agl'))