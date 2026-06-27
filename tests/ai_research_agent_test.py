from brain.ai_research_agent import AIResearchAgent


AIResearchAgent.show_models()

print("\nCoding Recommendation:")
print(
    AIResearchAgent.recommend_model("coding")
)

print("\nVision Recommendation:")
print(
    AIResearchAgent.recommend_model("vision")
)

print("\nWriting Recommendation:")
print(
    AIResearchAgent.recommend_model("writing")
)

print("\nOffline Recommendation:")
print(
    AIResearchAgent.recommend_model("offline")
)