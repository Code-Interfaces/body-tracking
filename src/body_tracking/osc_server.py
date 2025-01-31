from pythonosc.udp_client import SimpleUDPClient
from enum import Enum
from .config import config
from rich.console import Console
import logging

# Suppress Python-OSC logs
logging.getLogger("pythonosc").setLevel(logging.ERROR)

# Initialize Rich Console
console = Console()


class PoseLandmark(Enum):
    """Pose landmarks based on MediaPipe definitions."""

    # Face
    NOSE = 0
    LEFT_EYE_INNER = 1
    LEFT_EYE = 2
    LEFT_EYE_OUTER = 3
    RIGHT_EYE_INNER = 4
    RIGHT_EYE = 5
    RIGHT_EYE_OUTER = 6
    LEFT_EAR = 7
    RIGHT_EAR = 8
    MOUTH_LEFT = 9
    MOUTH_RIGHT = 10

    # Upper Body
    LEFT_SHOULDER = 11
    RIGHT_SHOULDER = 12
    LEFT_ELBOW = 13
    RIGHT_ELBOW = 14
    LEFT_WRIST = 15
    RIGHT_WRIST = 16

    # Lower Body
    LEFT_HIP = 23
    RIGHT_HIP = 24
    LEFT_KNEE = 25
    RIGHT_KNEE = 26
    LEFT_ANKLE = 27
    RIGHT_ANKLE = 28
    LEFT_HEEL = 29
    RIGHT_HEEL = 30
    LEFT_FOOT_INDEX = 31
    RIGHT_FOOT_INDEX = 32


class HandLandmark(Enum):
    """Hand landmarks based on MediaPipe definitions."""

    WRIST = 0
    THUMB_CMC = 1
    THUMB_MCP = 2
    THUMB_IP = 3
    THUMB_TIP = 4
    INDEX_FINGER_MCP = 5
    INDEX_FINGER_PIP = 6
    INDEX_FINGER_DIP = 7
    INDEX_FINGER_TIP = 8
    MIDDLE_FINGER_MCP = 9
    MIDDLE_FINGER_PIP = 10
    MIDDLE_FINGER_DIP = 11
    MIDDLE_FINGER_TIP = 12
    RING_FINGER_MCP = 13
    RING_FINGER_PIP = 14
    RING_FINGER_DIP = 15
    RING_FINGER_TIP = 16
    PINKY_MCP = 17
    PINKY_PIP = 18
    PINKY_DIP = 19
    PINKY_TIP = 20


class OSCSender:
    def __init__(self, ip=config.SERVER_IP, port=config.SERVER_PORT):
        """Initialize the OSC client with given IP and port."""
        self.client = SimpleUDPClient(ip, port)
        console.log(f"[bold green]✅ OSC client initialized with {
                    ip}:{port}[/bold green]")

    def send_landmarks(self, landmarks):
        """
        Send body pose landmarks via OSC.

        Args:
            landmarks: List of MediaPipe pose landmarks
        """
        if not landmarks:
            console.log(
                "[bold yellow]⚠️ No body landmarks detected[/bold yellow]")
            return

        for landmark in PoseLandmark:
            idx = landmark.value
            if idx < len(landmarks):
                point = landmarks[idx]
                osc_address = f"/pose/{landmark.name.lower()}"
                position = (point.x, point.y, point.z)

                console.log(f"📡 Sending: [cyan]{
                            osc_address}[/cyan] -> {position}")
                self.client.send_message(osc_address, position)

    def send_hand_landmarks(self, hands_landmarks):
        """
        Send hand landmarks via OSC.

        Args:
            hands_landmarks: List of hand landmarks detected by MediaPipe
        """
        if not hands_landmarks:
            console.log(
                "[bold yellow]⚠️ No hand landmarks detected[/bold yellow]")
            return

        for hand_idx, hand_landmarks in enumerate(hands_landmarks):
            for landmark in HandLandmark:
                idx = landmark.value
                if idx < len(hand_landmarks.landmark):
                    point = hand_landmarks.landmark[idx]
                    osc_address = f"/hand/{hand_idx}/{landmark.name.lower()}"
                    position = (point.x, point.y, point.z)
                    self.client.send_message(osc_address, position)

    def close(self):
        """Close the OSC sender (if necessary)."""
        console.log("[bold red]🛑 OSC sender closed.[/bold red]")
