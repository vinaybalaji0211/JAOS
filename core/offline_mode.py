import socket

from logs.logger import logger


class OfflineMode:

    @staticmethod
    def is_online():

        try:

            socket.create_connection(
                ("8.8.8.8", 53),
                timeout=3
            )

            logger.info(
                "Internet connection available."
            )

            return True

        except OSError:

            logger.warning(
                "Internet connection unavailable. Offline mode active."
            )

            return False

    @staticmethod
    def show_status():

        if OfflineMode.is_online():

            print("\nConnectivity: ONLINE")

        else:

            print("\nConnectivity: OFFLINE")