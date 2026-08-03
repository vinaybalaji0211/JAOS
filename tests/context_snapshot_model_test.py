from executive_brain.models.context_snapshot_model import ContextSnapshotModel

snapshot = ContextSnapshotModel(
    current_user="Vinay",
    active_project="JAOS",
    active_mode="DEVELOPMENT",
    active_ai_provider="OpenAI",
    internet_status="CONNECTED",
    system_status="HEALTHY"
)

snapshot.add_metadata(
    "active_window",
    "VS Code"
)

print()

print(snapshot.to_dict())