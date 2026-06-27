from brain.skill_library import (
    SkillLibrary
)

library = SkillLibrary()

library.add_skill(
    "YOLO Training",
    "Train and validate YOLO models"
)

library.add_skill(
    "VS Code Workflow",
    "Open project and run tests"
)

library.show_skills()