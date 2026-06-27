from brain.skill_system import SkillSystem


skills = SkillSystem()

skills.install_skill(

    "Memory Management",

    "Handles long-term memory operations"

)

skills.install_skill(

    "Planning",

    "Creates execution plans"

)

skills.install_skill(

    "Reasoning",

    "Performs high-level reasoning"

)

skills.show_skills()