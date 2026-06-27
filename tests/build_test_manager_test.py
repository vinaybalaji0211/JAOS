from development.build_test_manager import (
    BuildTestManager
)

manager = BuildTestManager()

manager.register_project(
    "JAOS",
    "python main.py",
    "python -m pytest"
)

manager.register_project(
    "YOLO Project",
    "python train.py",
    "python validate.py"
)

manager.show_projects()