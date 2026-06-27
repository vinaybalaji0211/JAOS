from kernel.kernel_health_monitor import (
    KernelHealthMonitor
)

monitor = KernelHealthMonitor()

monitor.update_status(
    "Memory Platform",
    "HEALTHY"
)

monitor.update_status(
    "Security Platform",
    "HEALTHY"
)

monitor.show_health()