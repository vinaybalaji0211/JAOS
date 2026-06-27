from logs.logger import logger


class CameraAwareness:

    def __init__(self):

        self.camera_available = False

        self.camera_enabled = False

        self.camera_status = "DISCONNECTED"

        self.last_frame = None

    def connect_camera(self):

        self.camera_available = True

        self.camera_status = "CONNECTED"

        logger.info(
            "Camera connected."
        )

    def enable_camera(self):

        if self.camera_available:

            self.camera_enabled = True

            self.camera_status = "ACTIVE"

            logger.info(
                "Camera enabled."
            )

    def disable_camera(self):

        self.camera_enabled = False

        if self.camera_available:

            self.camera_status = "CONNECTED"

        else:

            self.camera_status = "DISCONNECTED"

        logger.info(
            "Camera disabled."
        )

    def receive_frame(
            self,
            frame):

        if self.camera_enabled:

            self.last_frame = frame

            logger.info(
                "Camera frame received."
            )

            return "Frame received"

        return "Camera not enabled"

    def show_status(self):

        print("\nCamera Awareness:\n")

        print(
            f"Available: {self.camera_available}"
        )

        print(
            f"Enabled: {self.camera_enabled}"
        )

        print(
            f"Status: {self.camera_status}"
        )

        print(
            f"Last Frame: {self.last_frame}"
        )