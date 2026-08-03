import time

from core.performance_monitor import PerformanceMonitor

monitor = PerformanceMonitor()

monitor.start_timer()

time.sleep(2)

monitor.stop_timer()

monitor.show_duration()