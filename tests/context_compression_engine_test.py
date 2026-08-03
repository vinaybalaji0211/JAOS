from brain.context_compression_engine import ContextCompressionEngine

context = [
    "Step 76 complete",
    "Step 77 complete",
    "Step 78 complete",
    "Step 79 complete",
    "Step 80 complete",
    "Step 81 complete",
    "Step 82 complete"
]

ContextCompressionEngine.show_compressed(
    context,
    max_items=3
)