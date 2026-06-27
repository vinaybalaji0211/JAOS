import psutil


class HealthMonitor:

    @staticmethod
    def get_system_health():

        cpu = psutil.cpu_percent()

        memory = psutil.virtual_memory().percent

        disk = psutil.disk_usage('/').percent

        return {
            "CPU Usage": cpu,
            "Memory Usage": memory,
            "Disk Usage": disk
        }