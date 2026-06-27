from brain.unsupported_request_logger import (
    UnsupportedRequestLogger
)

logger = (
    UnsupportedRequestLogger()
)

logger.log_request(
    "Control Drone",
    "JAOS v7"
)

logger.log_request(
    "Smart Home Automation",
    "JAOS v7"
)

logger.log_request(
    "Mobile Companion",
    "JAOS v2"
)

logger.show_requests()