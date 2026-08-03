from brain.approval_based_upgrade_engine import ApprovalBasedUpgradeEngine

engine = ApprovalBasedUpgradeEngine()

engine.submit_upgrade(
    "Cloud Memory Architecture"
)

engine.submit_upgrade(
    "OCR Intelligence Engine"
)

engine.approve(
    "Cloud Memory Architecture"
)

engine.reject(
    "OCR Intelligence Engine"
)

engine.show_requests()