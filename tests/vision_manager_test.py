from brain.vision_manager import VisionManager

vision = VisionManager()

vision.show_modules()

vision.enable_module(
    "ocr_engine"
)

vision.enable_module(
    "screen_understanding"
)

vision.show_modules()