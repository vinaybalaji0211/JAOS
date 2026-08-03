from brain.object_registry import ObjectRegistry

registry = ObjectRegistry()

registry.register(

    "RTX3050",

    "GPU",

    {
        "vram": "4GB"
    }

)

registry.register(

    "OpenAI",

    "Provider"

)

registry.register(

    "Ultralytics",

    "Tool"

)

registry.register(

    "Build Independent AI OS",

    "Goal"

)

registry.show_registry()