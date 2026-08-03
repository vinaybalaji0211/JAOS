from core.recovery_tracker import RecoveryTracker

tracker = RecoveryTracker()

tracker.record_event(
    "Recovered snapshot after crash"
)

tracker.record_event(
    "Restarted engine successfully"
)

tracker.show_events()