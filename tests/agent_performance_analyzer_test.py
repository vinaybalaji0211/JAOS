from brain.agent_performance_analyzer import (
    AgentPerformanceAnalyzer
)

analyzer = AgentPerformanceAnalyzer()

analyzer.register_agent(
    "Research Agent"
)

analyzer.record_success(
    "Research Agent"
)

analyzer.record_success(
    "Research Agent"
)

analyzer.record_failure(
    "Research Agent"
)

analyzer.show_report()