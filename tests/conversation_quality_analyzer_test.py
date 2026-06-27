from brain.conversation_quality_analyzer import (
    ConversationQualityAnalyzer
)

analyzer = ConversationQualityAnalyzer()

analyzer.record_success()
analyzer.record_success()
analyzer.record_success()

analyzer.record_misunderstanding()

analyzer.show_report()