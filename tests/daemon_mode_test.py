from brain.daemon_mode import DaemonMode

daemon = DaemonMode()

daemon.show_status()

daemon.start()

daemon.show_status()

daemon.stop()

daemon.show_status()