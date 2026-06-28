from executive_brain.brain.executive_brain import ExecutiveBrain


def test_initialization():
    brain = ExecutiveBrain()

    assert brain.get_status() == "INITIALIZED"


def test_initialize():
    brain = ExecutiveBrain()

    assert brain.initialize() is True
    assert brain.get_status() == "READY"


def test_registry_manager_exists():
    brain = ExecutiveBrain()

    assert brain.get_registry_manager() is not None


def test_system_summary():
    brain = ExecutiveBrain()

    summary = brain.get_system_summary()

    assert summary["registry_manager"] is True
    assert isinstance(summary["registries"], list)
    assert isinstance(summary["registry_counts"], dict)


def test_health_check():
    brain = ExecutiveBrain()

    brain.initialize()

    health = brain.health_check()

    assert health["executive_brain"] is True
    assert health["registry_manager"]["intent"] is True