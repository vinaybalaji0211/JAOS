from brain.multi_microphone_support import MultiMicrophoneSupport

system = MultiMicrophoneSupport()

system.add_microphone(
    "Laptop Mic"
)

system.add_microphone(
    "USB Mic"
)

system.show_microphones()

system.remove_microphone(
    "Laptop Mic"
)

system.show_microphones()