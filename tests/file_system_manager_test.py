from pc_control.file_system_manager import FileSystemManager

manager = FileSystemManager()

manager.register_file(
    "Resume.pdf",
    "C:/Users/Vinay/Documents",
    "PDF"
)

manager.register_file(
    "JAOS.py",
    "C:/JARVIS",
    "Python"
)

manager.register_file(
    "Notes.txt",
    "C:/Users/Vinay/Desktop",
    "Text"
)

manager.show_files()

print(
    manager.get_file(
        "JAOS.py"
    )
)