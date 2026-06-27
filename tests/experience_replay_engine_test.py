from brain.experience_replay_engine import (
    ExperienceReplayEngine
)


experiences = [

    {
        "task": "YOLO training",

        "result": "FAILED",

        "lesson": "Use batch size 4"
    },

    {
        "task": "Provider selection",

        "result": "SUCCESS",

        "lesson": "Gemini works best"
    }

]

ExperienceReplayEngine.show_replay(
    experiences
)