from memory.memory_importance import MemoryImportance

memory_1 = (

    "Phase 3 goal completed successfully"

)

memory_2 = (

    "User opened VS Code"

)

memory_3 = (

    "Critical error detected"

)

print(

    "Memory 1 Score:",

    MemoryImportance.calculate(

        memory_1

    )

)

print(

    "Memory 2 Score:",

    MemoryImportance.calculate(

        memory_2

    )

)

print(

    "Memory 3 Score:",

    MemoryImportance.calculate(

        memory_3

    )

)