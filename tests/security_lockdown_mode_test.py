from brain.security_lockdown_mode import SecurityLockdownMode

system = SecurityLockdownMode()

system.show_status()

system.enter_lockdown()

system.show_status()

system.enter_recovery()

system.show_status()

system.reset_normal()

system.show_status()