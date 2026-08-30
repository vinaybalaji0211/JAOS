from executive_brain.pipeline.executive_pipeline import ExecutivePipeline


def test_pipeline_executes_request():
    pipeline = ExecutivePipeline()

    result = pipeline.execute("Hello JAOS")

    assert result["request"] == "Hello JAOS"
    assert result["result"] == "PIPELINE_EXECUTED"


def test_pipeline_reports_brain_ready():
    pipeline = ExecutivePipeline()

    result = pipeline.execute("Test")

    assert result["brain"] == "READY"


def test_pipeline_reports_memory_ready():
    pipeline = ExecutivePipeline()

    result = pipeline.execute("Test")

    assert result["memory"] == "READY"


def test_pipeline_reports_workflow_ready():
    pipeline = ExecutivePipeline()

    result = pipeline.execute("Test")

    assert result["workflow"] == "READY"