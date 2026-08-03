from brain.camera_awareness import CameraAwareness

camera = CameraAwareness()

camera.show_status()

camera.connect_camera()

camera.enable_camera()

print(
    camera.receive_frame(
        "sample_frame_001"
    )
)

camera.show_status()