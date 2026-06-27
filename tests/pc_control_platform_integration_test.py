from pc_control.application_manager import ApplicationManager
from pc_control.window_manager import WindowManager
from pc_control.file_system_manager import FileSystemManager
from pc_control.terminal_controller import TerminalController
from pc_control.browser_controller import BrowserController
from pc_control.system_monitor import SystemMonitor
from pc_control.notification_manager import NotificationManager

print("\n===== PC CONTROL PLATFORM TEST =====\n")

app = ApplicationManager()
app.register_application("VS Code", "Code.exe")

window = WindowManager()
window.register_window("VS Code - JAOS", "VS Code")

files = FileSystemManager()
files.register_file(
    "main.py",
    "C:/JARVIS",
    "Python"
)

terminal = TerminalController()
terminal.register_command("python main.py")

browser = BrowserController()
browser.register_session(
    "Chrome",
    "https://github.com"
)

system = SystemMonitor()
system.update_metric("CPU", "28%")
system.update_metric("RAM", "46%")

notify = NotificationManager()
notify.add_notification(
    "SUCCESS",
    "Platform Test Started"
)

print("\n===== COMPONENT STATUS =====\n")

app.show_applications()
window.show_windows()
files.show_files()
terminal.show_commands()
browser.show_sessions()
system.show_metrics()
notify.show_notifications()

print("\n===== PC CONTROL PLATFORM COMPLETE =====")