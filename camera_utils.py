import numpy as np
import cv2
import time

def simulate_camera(self):
    # Open the default camera (usually 0)
    cap = cv2.VideoCapture(0)

    while self.running:
        if self.camera_active:
            ret, frame = cap.read()
            if ret:
                self.window.after(0, self.update_camera_feed, frame)
        time.sleep(0.03)  # ~30 fps

    # Release the camera when done
    cap.release()



