from knowledge.research_manager import ResearchManager

manager = ResearchManager()

manager.register_project(
    "Underwater Detection",
    "YOLO Object Detection"
)

manager.register_project(
    "JAOS Research",
    "AI Operating Systems"
)

manager.show_projects()