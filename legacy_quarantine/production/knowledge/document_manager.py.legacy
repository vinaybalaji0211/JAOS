from logs.logger import logger


class DocumentManager:

    def __init__(self):

        self.documents = {}

    def register_document(
            self,
            name,
            path,
            document_type):

        self.documents[name] = {
            "path": path,
            "type": document_type
        }

        logger.info(
            f"Document registered: {name}"
        )

    def show_documents(self):

        print("\n=== Document Manager ===\n")

        if not self.documents:

            print("No documents.")
            return

        for name, data in self.documents.items():

            print(name)
            print(f"  Path : {data['path']}")
            print(f"  Type : {data['type']}")
            print()