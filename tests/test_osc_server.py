import pytest
from body_tracking.osc_server import OSCSender


@pytest.fixture
def osc_sender():
    return OSCSender()


def test_osc_initialization(osc_sender):
    assert osc_sender.client is not None


def test_osc_send_landmarks(osc_sender):
    test_landmarks = [{"x": 0.5, "y": 0.6, "z": 0.7}]
    try:
        osc_sender.send_landmarks(test_landmarks)
        success = True
    except Exception:
        success = False
    assert success
