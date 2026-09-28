from logs.logger import logger


class TransparencyLayer:

    @staticmethod
    def show_report(title, data):

        print(f"\n{title}:")

        if not data:

            print("No data available.")

        elif isinstance(data, dict):

            for key, value in data.items():

                print(f"{key}: {value}")

        elif isinstance(data, list):

            for index, item in enumerate(
                    data,
                    start=1):

                print(f"{index}. {item}")

        else:

            print(data)

        logger.info(
            f"Transparency report shown: {title}"
        )