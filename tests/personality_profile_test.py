from brain.personality_profile import (
    PersonalityProfile
)

personality = PersonalityProfile()

personality.update(
    "proactivity",
    1.0
)

personality.update(
    "humor",
    0.3
)

personality.show_profile()