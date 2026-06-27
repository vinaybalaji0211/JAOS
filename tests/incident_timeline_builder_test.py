from brain.incident_timeline_builder import (
    IncidentTimelineBuilder
)

builder = (
    IncidentTimelineBuilder()
)

builder.add_event(
    "10:01",
    "Unauthorized Login Attempt"
)

builder.add_event(
    "10:03",
    "Safe Mode Activated"
)

builder.add_event(
    "10:05",
    "Threat Resolved"
)

builder.show_timeline()