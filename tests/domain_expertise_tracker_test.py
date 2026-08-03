from brain.domain_expertise_tracker import DomainExpertiseTracker

tracker = (
    DomainExpertiseTracker()
)

tracker.update_expertise(
    "Quantum Physics",
    45
)

tracker.update_expertise(
    "Cybersecurity",
    80
)

tracker.update_expertise(
    "Machine Learning",
    92
)

tracker.show_expertise()

print(
    tracker.get_expertise(
        "Cybersecurity"
    )
)