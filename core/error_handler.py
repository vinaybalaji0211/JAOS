from logs.logger import logger


class ErrorHandler:

    @staticmethod
    def handle_error(error):

        logger.error(f"Error occurred: {error}")

        print("Error:", error)