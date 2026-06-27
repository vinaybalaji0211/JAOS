from logs.logger import logger


class OCREngine:

    def __init__(self):

        self.enabled = True

        self.supported_inputs = [
            "image",
            "screenshot",
            "document",
            "screen"
        ]

    def read_text(
            self,
            input_source):

        logger.info(
            f"OCR requested for: {input_source}"
        )

        return (
            "OCR placeholder text. "
            "Real OCR engine will be connected later."
        )

    def show_status(self):

        print("\nOCR Engine:\n")

        print(
            f"Enabled: {self.enabled}"
        )

        print(
            f"Supported Inputs: {self.supported_inputs}"
        )