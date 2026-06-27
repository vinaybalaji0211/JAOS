from logs.logger import logger


class ScreenUnderstanding:

    @staticmethod
    def analyze_screen(
            ocr_text,
            active_window,
            visible_elements):

        summary = {
            "active_window": active_window,
            "ocr_text": ocr_text,
            "visible_elements": visible_elements,
            "possible_actions": []
        }

        text_lower = ocr_text.lower()

        if "error" in text_lower:
            summary["possible_actions"].append(
                "Investigate error message"
            )

        if "login" in text_lower:
            summary["possible_actions"].append(
                "Check login form"
            )

        if "run" in text_lower:
            summary["possible_actions"].append(
                "Possible command execution"
            )

        if not summary["possible_actions"]:
            summary["possible_actions"].append(
                "Observe screen"
            )

        logger.info(
            "Screen understanding completed."
        )

        return summary

    @staticmethod
    def show_analysis(
            ocr_text,
            active_window,
            visible_elements):

        result = ScreenUnderstanding.analyze_screen(
            ocr_text,
            active_window,
            visible_elements
        )

        print("\nScreen Understanding:\n")

        print(
            f"Active Window: {result['active_window']}"
        )

        print(
            f"OCR Text: {result['ocr_text']}"
        )

        print(
            f"Visible Elements: {result['visible_elements']}"
        )

        print("\nPossible Actions:")

        for action in result["possible_actions"]:

            print(
                f"- {action}"
            )