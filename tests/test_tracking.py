import pytest
import cv2
from body_tracking.tracking import BodyTracker


@pytest.fixture
def tracker():
    return BodyTracker()


def test_tracking_initialization(tracker):
    assert tracker.pose is not None


def test_tracking_process_frame(tracker):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if ret:
        landmarks = tracker.track(frame)
        assert landmarks is None or isinstance(landmarks, list)
