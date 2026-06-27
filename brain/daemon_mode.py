from logs.logger import logger


class DaemonMode:

    def __init__(self):
        self.running = False
        self.mode = "STOPPED"

    def start(self):
        self.running = True
        self.mode = "RUNNING"
        logger.info("Daemon mode started.")

    def stop(self):
        self.running = False
        self.mode = "STOPPED"
        logger.info("Daemon mode stopped.")

    def status(self):
        return {
            "running": self.running,
            "mode": self.mode
        }

    def show_status(self):
        print("\nDaemon Mode:\n")
        print(f"Running: {self.running}")
        print(f"Mode: {self.mode}")