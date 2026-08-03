from memory.memory_safety import MemorySafety

memory_1 = (

    "Phase 3 architecture completed"

)

memory_2 = (

    "User password is abc123"

)

print(

    MemorySafety.is_safe(

        memory_1

    )

)

print(

    MemorySafety.is_safe(

        memory_2

    )

)

MemorySafety.explain(

    memory_2

)