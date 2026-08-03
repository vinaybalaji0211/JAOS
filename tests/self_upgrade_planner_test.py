from brain.self_upgrade_planner import SelfUpgradePlanner

planner = SelfUpgradePlanner()

planner.create_plan(
    "Cloud Memory Architecture",
    [
        "Create storage layer",
        "Create sync manager",
        "Add authentication",
        "Run tests",
        "Prepare deployment"
    ]
)

planner.show_plan(
    "Cloud Memory Architecture"
)