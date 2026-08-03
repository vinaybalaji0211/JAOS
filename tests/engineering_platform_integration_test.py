from engineering.capability_truth_engine import CapabilityTruthEngine
from engineering.configuration_validator import ConfigurationValidator
from engineering.dependency_validator import DependencyValidator
from engineering.engineering_report_generator import EngineeringReportGenerator
from engineering.import_validator import ImportValidator
from engineering.integration_test_runner import IntegrationTestRunner
from engineering.module_registry import ModuleRegistry
from engineering.package_registry import PackageRegistry
from engineering.platform_health_dashboard import PlatformHealthDashboard
from engineering.platform_registry import PlatformRegistry
from engineering.project_structure_validator import ProjectStructureValidator
from engineering.startup_validator import StartupValidator

print("\n========== ENGINEERING PLATFORM TEST ==========\n")

ProjectStructureValidator().validate()

module_registry = ModuleRegistry()
module_registry.register_module(
    "Memory Manager",
    "Memory",
    "v1 Alpha"
)

platform_registry = PlatformRegistry()
platform_registry.register_platform(
    "Security",
    "v1 Alpha",
    "ACTIVE",
    True
)

package_registry = PackageRegistry()
package_registry.register_package(
    "torch",
    "2.5.1"
)

dependency_validator = DependencyValidator()
dependency_validator.add_dependency(
    "Workflow",
    "Memory"
)

import_validator = ImportValidator()
import_validator.add_import(
    "security.permission_manager"
)

configuration_validator = ConfigurationValidator()
configuration_validator.add_required_key(
    "theme"
)
configuration_validator.set_config(
    "theme",
    "dark"
)

startup_validator = StartupValidator()
startup_validator.add_required_service(
    "JAOS Core"
)
startup_validator.register_service(
    "JAOS Core"
)

runner = IntegrationTestRunner()
runner.register_test(
    "Security Platform"
)

health = PlatformHealthDashboard()
health.update_platform(
    "Security",
    "HEALTHY",
    20,
    0,
    True
)

truth = CapabilityTruthEngine()
truth.register_capability(
    "Open VS Code",
    "PC Control",
    True,
    "v1 Alpha"
)

report = EngineeringReportGenerator()
report.add_section(
    "Engineering",
    "PASS"
)

print("\n========== SUMMARY ==========\n")

module_registry.show_modules()

platform_registry.show_platforms()

package_registry.show_packages()

dependency_validator.validate()

import_validator.validate()

configuration_validator.validate()

startup_validator.validate()

runner.run_tests()

runner.show_summary()

health.show_dashboard()

truth.show_capabilities()

report.generate_report()

print("\n========== ENGINEERING PLATFORM COMPLETE ==========")