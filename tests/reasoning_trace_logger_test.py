from brain.reasoning_trace_logger import ReasoningTraceLogger


ReasoningTraceLogger.record(
    "Use memory search",
    "The user asked about previous project progress"
)

ReasoningTraceLogger.record(
    "Proceed to Phase 3 Step 20",
    "All previous Phase 3 brain and memory components are ready"
)

ReasoningTraceLogger.show()