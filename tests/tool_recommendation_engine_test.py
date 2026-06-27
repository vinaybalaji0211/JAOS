from brain.tool_recommendation_engine import (
    ToolRecommendationEngine
)


missing_capabilities = [

    "vision",

    "web_search",

    "device_control",

    "research"

]

ToolRecommendationEngine.show_recommendations(

    missing_capabilities

)