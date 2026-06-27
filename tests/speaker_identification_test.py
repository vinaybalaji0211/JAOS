from brain.speaker_identification import (
    SpeakerIdentification
)

system = SpeakerIdentification()

system.register_speaker(
    "Vinay",
    "AUTHOR"
)

system.register_speaker(
    "FamilyMember",
    "TRUSTED"
)

system.show_identification(
    "Vinay"
)

system.show_identification(
    "FamilyMember"
)

system.show_identification(
    "UnknownPerson"
)