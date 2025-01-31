import logging
import os
import mediapipe as mp
import cv2

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


class HandTracker:
    def __init__(self):
        """Initialize MediaPipe Hands model."""
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands()

    def track(self, frame):
        """Process a frame and return hand landmarks."""
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image_rgb)
        return results  # Returns None if no hands detected

    def close(self):
        """Close the MediaPipe Hands model."""
        self.hands.close()
