from brain.human_approval_layer import HumanApprovalLayer

HumanApprovalLayer.show_request(
    "RUN_DIAGNOSTICS",
    "ALLOW"
)

HumanApprovalLayer.show_request(
    "INSTALL_PACKAGE",
    "REQUIRE_APPROVAL"
)

HumanApprovalLayer.show_request(
    "DELETE_FILE",
    "BLOCK"
)