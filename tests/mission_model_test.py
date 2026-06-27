from executive_brain.models.mission_model import MissionModel

mission = MissionModel(
    mission_name="Launch VS Code",
    related_goal_id="GOAL-001",
    total_steps=3,
    steps=[
        "Check VS Code installation",
        "Launch VS Code",
        "Verify process started"
    ]
)

mission.update_progress(33.3)

mission.add_metadata(
    "step_description",
    "Checking installation"
)

print()
print(mission.to_dict())