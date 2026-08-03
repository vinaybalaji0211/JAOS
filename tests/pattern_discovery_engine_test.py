from brain.pattern_discovery_engine import PatternDiscoveryEngine

events = [

    "GPU OOM",

    "GPU OOM",

    "Gemini success",

    "GPU OOM",

    "OpenAI success",

    "Gemini success"

]

PatternDiscoveryEngine.show_patterns(
    events
)