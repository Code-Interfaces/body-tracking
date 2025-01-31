import logging
import os
import mediapipe as mp

# Suppress TensorFlow Lite warnings
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
logging.getLogger("mediapipe").setLevel(logging.ERROR)
logging.getLogger("cv2").setLevel(logging.ERROR)


class BodyTracker:
    def __init__(self):
        """Initialize MediaPipe Pose model."""
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(static_image_mode=False,
                                      min_detection_confidence=0.5, model_complexity=1)
        self.mp_drawing = mp.solutions.drawing_utils

    def track(self, frame):
        """Process a frame and return pose landmarks."""

        results = self.pose.process(frame)

        if results.pose_landmarks:
            return results
        return None

    def close(self):
        """Close the MediaPipe model."""
        self.pose.close()
