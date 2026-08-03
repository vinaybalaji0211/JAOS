from brain.self_improvement_analyzer import SelfImprovementAnalyzer

analyzer = SelfImprovementAnalyzer()

analyzer.add_weakness(
    "Cloud Memory Architecture Missing",
    "HIGH"
)

analyzer.add_weakness(
    "OCR Intelligence Engine Missing",
    "HIGH"
)

analyzer.add_weakness(
    "Agent Reputation System Missing",
    "MEDIUM"
)

analyzer.show_analysis()