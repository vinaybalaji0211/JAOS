from kernel.kernel_lifecycle_manager import KernelLifecycleManager

manager = KernelLifecycleManager()

manager.register_platform("Memory Platform")
manager.register_platform("Security Platform")

manager.start_platform("Memory Platform")
manager.start_platform("Security Platform")

manager.show_status()

manager.stop_platform("Security Platform")

print("\nAfter stopping Security Platform:\n")

manager.show_status()