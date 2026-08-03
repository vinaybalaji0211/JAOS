from brain.application_skill_learner import ApplicationSkillLearner

learner = ApplicationSkillLearner()

learner.learn_application(
    "VS Code",
    "Open project and run Python scripts"
)

learner.learn_application(
    "Chrome",
    "Navigate websites and manage tabs"
)

learner.show_applications()