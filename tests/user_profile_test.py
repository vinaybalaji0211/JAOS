from brain.user_profile import UserProfile

profile = {

    "name": "Vinay",

    "project": "JARVIS OS",

    "goal":

    "Build an independent 24/7 AI Operating System"

}

UserProfile.save(
    profile
)

UserProfile.show()