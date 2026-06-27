from knowledge.ocr_manager import OCRManager

ocr = OCRManager()

ocr.register_job(
    "research_paper.pdf",
    "Extracted OCR text..."
)

ocr.register_job(
    "whiteboard.jpg",
    "Meeting notes from whiteboard."
)

ocr.show_jobs()