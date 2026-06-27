from datetime import datetime


class EngineeringReportGenerator:

    def __init__(self):

        self.sections = []

    def add_section(
            self,
            title,
            status):

        self.sections.append({

            "title": title,

            "status": status

        })

    def generate_report(self):

        print("\n========== ENGINEERING REPORT ==========\n")

        print(
            f"Generated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

        print()

        passed = 0

        failed = 0

        for section in self.sections:

            print(
                f"{section['title']} : {section['status']}"
            )

            if section["status"] == "PASS":

                passed += 1

            else:

                failed += 1

        print()

        print(f"Passed : {passed}")

        print(f"Failed : {failed}")

        if failed == 0:

            print("\nEngineering Status : READY")

        else:

            print("\nEngineering Status : NOT READY")