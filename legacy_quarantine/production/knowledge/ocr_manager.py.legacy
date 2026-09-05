from logs.logger import logger


class OCRManager:

    def __init__(self):

        self.jobs = {}

    def register_job(
            self,
            document,
            extracted_text,
            status="COMPLETED"):

        self.jobs[document] = {
            "text": extracted_text,
            "status": status
        }

        logger.info(
            f"OCR job registered: {document}"
        )

    def show_jobs(self):

        print("\n=== OCR Manager ===\n")

        if not self.jobs:

            print("No OCR jobs.")
            return

        for document, data in self.jobs.items():

            print(document)
            print(f"  Status : {data['status']}")
            print(f"  Text   : {data['text']}")
            print()