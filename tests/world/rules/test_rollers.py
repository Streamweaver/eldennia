import random

from evennia.utils.test_resources import EvenniaTest

from world.rules import rollers
class RollerTestCase(EvenniaTest):

    def test_simple_check(self):
        for _ in range(10000):
            i = random.randrange(0, 15)
            self.assertIn(rollers.simple_check(i), [True, False])

    def test_roll_attribute(self):
        for _ in range(10000):
            i = random.randrange(0, 15)
            actual = rollers.roll_attribute(i)
            self.assertTrue(-1 <=  actual <= 15, msg=actual)