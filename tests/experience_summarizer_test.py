from brain.experience_summarizer import (
    ExperienceSummarizer
)


experiences = [
    {
        "event": "Plugin installation",
        "result": "SUCCESS",
        "lesson": "Trust validation works."
    },
    {
        "event": "Security attack",
        "result": "FAILURE",
        "lesson": "Need stronger threat monitoring."
    }
]

ExperienceSummarizer.show_summary(
    experiences
)