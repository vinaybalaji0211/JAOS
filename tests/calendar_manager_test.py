from communication.calendar_manager import (
    CalendarManager
)

calendar = CalendarManager()

calendar.add_event(
    "JAOS Development",
    "Today 7:00 PM"
)

calendar.add_event(
    "Project Review",
    "Tomorrow 10:00 AM"
)

calendar.show_events()