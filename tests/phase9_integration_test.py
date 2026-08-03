from brain.camera_awareness import CameraAwareness
from brain.gui_agent import GUIAgent
from brain.ocr_engine import OCREngine
from brain.screen_understanding import ScreenUnderstanding
from brain.vision_manager import VisionManager
from brain.visual_memory import VisualMemory

print("\n=== PHASE 9 INTEGRATION TEST ===\n")

# Vision Manager
vision = VisionManager()

vision.enable_module(
    "ocr_engine"
)

vision.enable_module(
    "screen_understanding"
)

vision.enable_module(
    "gui_agent"
)

vision.enable_module(
    "camera_awareness"
)

vision.enable_module(
    "visual_memory"
)

vision.show_modules()

# OCR
ocr = OCREngine()

text = ocr.read_text(
    "screen"
)

print(
    "\nOCR Output:"
)

print(
    text
)

# Screen Understanding

ScreenUnderstanding.show_analysis(

    ocr_text=text,

    active_window="VS Code",

    visible_elements=[

        "terminal",

        "editor"

    ]

)

# GUI Agent

agent = GUIAgent()

print()

print(

    agent.execute(

        "open",

        "Command Prompt"

    )

)

# Camera

camera = CameraAwareness()

camera.connect_camera()

camera.enable_camera()

camera.receive_frame(

    "frame_001"

)

camera.show_status()

# Visual Memory

memory = VisualMemory()

memory.remember(

    "screen_text",

    text

)

memory.remember(

    "camera_frame",

    "frame_001"

)

memory.remember(

    "gui_state",

    "VS Code active"

)

memory.show_memories()

print("\n=== PHASE 9 COMPLETE ===")