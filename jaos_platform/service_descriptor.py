from dataclasses import dataclass

from jaos_platform.service_lifetime import ServiceLifetime


@dataclass(slots=True)
class ServiceDescriptor:
    name: str
    implementation: object
    lifetime: ServiceLifetime