from logs.logger import logger


class VisionManager:

    def __init__(self):

        self.modules = {

            "ocr_engine": False,

            "screen_understanding": False,

            "gui_agent": False,

            "camera_awareness": False,

            "visual_memory": False

        }

    def enable_module(
            self,
            module_name):

        if module_name in self.modules:

            self.modules[module_name] = True

            logger.info(
                f"{module_name} enabled."
            )

    def disable_module(
            self,
            module_name):

        if module_name in self.modules:

            self.modules[module_name] = False

            logger.info(
                f"{module_name} disabled."
            )

    def show_modules(self):

        print("\nVision Manager:\n")

        for module, status in self.modules.items():

            state = (
                "ENABLED"
                if status
                else "DISABLED"
            )

            print(
                f"{module}: {state}"
            )