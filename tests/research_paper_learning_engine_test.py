from brain.research_paper_learning_engine import ResearchPaperLearningEngine

engine = (
    ResearchPaperLearningEngine()
)

engine.learn_paper(
    "Attention Is All You Need",
    "Transformer Models"
)

engine.learn_paper(
    "YOLOv8 Object Detection",
    "Computer Vision"
)

engine.learn_paper(
    "Quantum Error Correction",
    "Quantum Computing"
)

engine.show_papers()