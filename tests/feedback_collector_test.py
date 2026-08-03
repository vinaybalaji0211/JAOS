from brain.feedback_collector import FeedbackCollector

collector = FeedbackCollector()

collector.add_experience(

    task="Train YOLO model",

    result="FAILED",

    reason="GPU memory insufficient",

    lesson="Reduce batch size",

    next_action="Use batch=4",

    confidence=72,

    provider="OpenAI"

)

collector.add_experience(

    task="Provider selection",

    result="SUCCESS",

    reason="Correct routing",

    lesson="Use Gemini for reasoning",

    next_action="Reuse strategy",

    confidence=95,

    provider="Gemini"

)

collector.show_experiences()