from brain.self_code_generator import SelfCodeGenerator

generator = SelfCodeGenerator()

generator.generate(
    "Cloud Memory Architecture",
    "Generate cloud storage synchronization module"
)

generator.generate(
    "OCR Intelligence Engine",
    "Generate OCR document extraction module"
)

generator.show_generated_code()