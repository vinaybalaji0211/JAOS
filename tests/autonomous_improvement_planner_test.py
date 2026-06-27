from brain.autonomous_improvement_planner import (
    AutonomousImprovementPlanner
)


AutonomousImprovementPlanner.show_plan(

    repeated_failures=[

        "GPU memory overflow"

    ],

    missing_capabilities=[

        "vision"

    ],

    curiosity_questions=[

        "How can I acquire vision capability?",

        "What should I learn about computer vision?"

    ]

)