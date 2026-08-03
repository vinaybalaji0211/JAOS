from pc_control.system_monitor import SystemMonitor

monitor = SystemMonitor()

monitor.update_metric(
    "CPU",
    "32%"
)

monitor.update_metric(
    "RAM",
    "58%"
)

monitor.update_metric(
    "GPU",
    "21%"
)

monitor.update_metric(
    "Battery",
    "Charging"
)

monitor.show_metrics()