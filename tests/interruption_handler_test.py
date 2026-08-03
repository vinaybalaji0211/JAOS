from brain.interruption_handler import InterruptionHandler

handler = InterruptionHandler()

handler.start_task(
    "Explaining Executive Brain"
)

handler.show_status()

handler.interrupt(
    "User new command"
)

handler.show_status()

handler.start_task(
    "Answer interruption"
)

handler.show_status()

handler.resume()

handler.show_status()