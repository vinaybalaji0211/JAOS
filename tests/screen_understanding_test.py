from brain.screen_understanding import (
    ScreenUnderstanding
)


ScreenUnderstanding.show_analysis(
    ocr_text="Error: Module not found. Run command failed.",
    active_window="Command Prompt",
    visible_elements=[
        "terminal",
        "error text",
        "command line"
    ]
)