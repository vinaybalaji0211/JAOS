from logs.logger import logger


class BootPhaseManager:

    def __init__(self):

        self.phases = {
            "PRE_BOOT": [],
            "CORE_BOOT": [],
            "KERNEL_BOOT": [],
            "PLATFORM_BOOT": [],
            "SERVICE_BOOT": [],
            "AI_BOOT": [],
            "EXPERIENCE_BOOT": [],
            "READY": []
        }

    def register_step(
            self,
            phase,
            step):

        if phase not in self.phases:
            self.phases[phase] = []

        self.phases[phase].append(step)

        logger.info(
            f"Boot phase step registered: {phase} -> {step}"
        )

    def run_boot(self):

        print("\n========== JAOS PHASED BOOT ==========\n")

        for phase, steps in self.phases.items():

            print(f"\n[{phase}]")

            if not steps:
                print("  No steps.")
                continue

            for step in steps:
                print(f"  ✓ {step}")

                logger.info(
                    f"Boot phase completed: {phase} -> {step}"
                )

        print("\nJAOS Phased Boot Completed Successfully.\n")