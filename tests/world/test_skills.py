from evennia.utils.test_resources import EvenniaTest

from ainneve.world.skills import Skill, SkillException

from typeclasses.characters import Character
from world.skills import load_skill, SKILL_LIST, AGL_SKILLS, STR_SKILLS, KNW_SKILLS, PER_SKILLS, TCH_SKILLS, MCH_SKILLS

class SkillsTestCase(EvenniaTest):
    character_typeclass = Character

    def test_skill_data(self):
        "Not really a unit test, I just want to make sure skill data validates"
        stat_skills = set()
        stat_skills.update(AGL_SKILLS, STR_SKILLS, KNW_SKILLS, MCH_SKILLS, PER_SKILLS, TCH_SKILLS)
        skill_list = set(SKILL_LIST)
        missmatches1 = list(stat_skills - skill_list)
        self.assertEqual(len(missmatches1), 0, msg=missmatches1)
        missmatches2 = list(skill_list - stat_skills)
        self.assertEqual(len(missmatches2), 0, msg=missmatches2)

    def test_load_skill(self):
        skill_test = ['robotics', 'dodge']
        for skill in skill_test:
            sk = load_skill(skill)
            self.assertIsInstance(sk, Skill)

        self.assertRaises(SkillException, load_skill, "noskill")
