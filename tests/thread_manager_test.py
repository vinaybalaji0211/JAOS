import time

from core.thread_manager import ThreadManager


def background_task():

    print("Background task started")

    time.sleep(2)

    print("Background task completed")


manager = ThreadManager()

manager.run_in_thread(
    background_task,
    "TestThread"
)

manager.show_threads()

manager.wait_for_all()

manager.show_threads()