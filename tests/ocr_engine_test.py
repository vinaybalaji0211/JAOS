from brain.ocr_engine import OCREngine


ocr = OCREngine()

ocr.show_status()

text = ocr.read_text(
    "screenshot"
)

print("\nExtracted Text:")

print(text)