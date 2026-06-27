from logs.logger import logger


class Diagnostics:

    @staticmethod
    def run_diagnostics(
            modules,
            events,
            plugins,
            health):

        report = {

            "Engine": "ONLINE",

            "Modules Loaded": len(modules),

            "Events Recorded": len(events),

            "Plugins Loaded": len(plugins),

            "CPU Usage": health["CPU Usage"],

            "Memory Usage": health["Memory Usage"],

            "Disk Usage": health["Disk Usage"]

        }

        logger.info("Diagnostics completed.")

        return report