from brain.skill_marketplace import SkillMarketplace

market = SkillMarketplace()

market.add_skill(
    "Weather Skill",
    "1.0"
)

market.add_skill(
    "Translator Skill",
    "1.0"
)

market.show_skills()

market.remove_skill(
    "Weather Skill"
)

market.show_skills()