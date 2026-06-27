from brain.environment_graph import (
    EnvironmentGraph
)

graph = EnvironmentGraph()

graph.add_relationship(

    "Build Independent AI OS",

    "contains",

    "Phase 5 World Model"

)

graph.add_relationship(

    "Phase 5 World Model",

    "contains",

    "Train YOLO"

)

graph.add_relationship(

    "Train YOLO",

    "uses",

    "Ultralytics"

)

graph.add_relationship(

    "Ultralytics",

    "runs_on",

    "RTX3050"

)

graph.show_graph()