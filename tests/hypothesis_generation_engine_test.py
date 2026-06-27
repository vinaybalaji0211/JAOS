from brain.hypothesis_generation_engine import (
    HypothesisGenerationEngine
)

engine = (
    HypothesisGenerationEngine()
)

engine.generate(
    "YOLO Training Slow",
    [
        "GPU utilization is low",
        "Data loading bottleneck",
        "Image size is too large",
        "Disk is too slow",
        "Background applications consuming VRAM"
    ]
)

engine.show_hypotheses(
    "YOLO Training Slow"
)