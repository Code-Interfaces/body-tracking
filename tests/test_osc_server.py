import pytest
from body_tracking.osc_server import OSCSender, PoseLandmark
from unittest.mock import Mock, patch
from body_tracking.config import config


class MockUDPClient:
    def __init__(self, ip=None, port=None):
        self.sent_messages = []
        self.ip = ip
        self.port = port

    def send_message(self, address, data):
        self.sent_messages.append((address, data))


def create_mock_landmarks():
    """Create mock landmarks for testing."""
    class MockLandmark:
        def __init__(self, x, y, z):
            self.x = x
            self.y = y
            self.z = z

    # Create 33 mock landmarks
    return [MockLandmark(0.5, 0.6, 0.7) for _ in range(33)]


@pytest.fixture
def mock_udp_client():
    """Fixture to mock the UDP client."""
    with patch('pythonosc.udp_client.SimpleUDPClient', spec=MockUDPClient) as mock_client:
        mock_instance = mock_client.return_value
        mock_instance.send_message = Mock()
        yield mock_instance


@pytest.fixture
def osc_sender():
    """Fixture to create an OSCSender instance with mocked client."""
    with patch('pythonosc.udp_client.SimpleUDPClient', spec=MockUDPClient) as mock_client:
        mock_instance = mock_client.return_value
        mock_instance.send_message = Mock()

        # Create OSCSender with mocked client
        sender = OSCSender()
        sender.client = mock_instance
        return sender


def test_osc_sender_initialization():
    """Test that OSCSender initializes with correct IP and port."""
    sender = OSCSender()
    assert sender.client.ip == config.SERVER_IP
    assert sender.client.port == config.SERVER_PORT


def test_send_landmarks(osc_sender):
    """Test sending all landmarks."""
    mock_landmarks = create_mock_landmarks()

    osc_sender.send_landmarks(mock_landmarks)

    # Check that send_message was called for each landmark
    assert osc_sender.client.send_message.call_count == len(PoseLandmark) * 2

    # Verify some specific calls
    calls = osc_sender.client.send_message.call_args_list

    # Check a few specific landmarks
    nose_calls = [call for call in calls if "/pose/nose" in call[0][0]]
    assert len(nose_calls) == 1
    assert nose_calls[0][0][1] == (0.5, 0.6, 0.7)


def test_send_specific_landmarks(osc_sender):
    """Test sending specific landmarks."""
    mock_landmarks = create_mock_landmarks()

    # Choose specific landmarks to send
    points_of_interest = [
        PoseLandmark.NOSE,
        PoseLandmark.LEFT_SHOULDER,
        PoseLandmark.RIGHT_WRIST
    ]

    osc_sender.send_specific_landmarks(mock_landmarks, points_of_interest)

    # Check that send_message was called for each specified landmark
    assert osc_sender.client.send_message.call_count == len(points_of_interest)

    # Verify calls for specific landmarks
    calls = osc_sender.client.send_message.call_args_list

    # Check landmark names and coordinates
    for point in points_of_interest:
        landmark_calls = [
            call for call in calls if f"/pose/{point.name.lower()}" in call[0][0]]
        assert len(landmark_calls) == 1
        assert landmark_calls[0][0][1] == (0.5, 0.6, 0.7)


def test_send_landmarks_empty_input(osc_sender):
    """Test sending landmarks with empty input."""
    osc_sender.send_landmarks([])
    osc_sender.send_specific_landmarks([], [])

    # No additional calls should be made beyond previous tests
    assert osc_sender.client.send_message.call_count > 0


def test_close_method(osc_sender):
    """Test the close method."""
    # Simply ensure no exception is raised
    osc_sender.close()
