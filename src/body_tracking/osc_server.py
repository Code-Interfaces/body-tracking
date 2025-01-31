from pythonosc.udp_client import SimpleUDPClient
from enum import Enum
from .config import config
from rich.console import Console
from rich.table import Table

# Initialize Rich Console
console = Console()


class PoseLandmark(Enum):
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

    # Hands
    LEFT_PINKY = 17
    RIGHT_PINKY = 18
    LEFT_INDEX = 19
    RIGHT_INDEX = 20
    LEFT_THUMB = 21
    RIGHT_THUMB = 22

    # Lower Body
    LEFT_HIP = 23
    RIGHT_HIP = 24
    LEFT_KNEE = 25
    RIGHT_KNEE = 26
    LEFT_ANKLE = 27
    RIGHT_ANKLE = 28

    # Feet
    LEFT_HEEL = 29
    RIGHT_HEEL = 30
    LEFT_FOOT_INDEX = 31
    RIGHT_FOOT_INDEX = 32


class OSCSender:
    def __init__(self, ip=config.SERVER_IP, port=config.SERVER_PORT):
        """Initialize the OSC client with given IP and port."""
        self.client = SimpleUDPClient(ip, port)
        console.log(f"[bold green]✅ OSC client initialized with {
                    ip}:{port}[/bold green]")

    def send_landmarks(self, landmarks):
        """
        Send pose landmarks via OSC using descriptive names.

        Args:
            landmarks: List of MediaPipe pose landmarks
        """
        if not landmarks:
            console.log("[bold yellow]⚠️ No landmarks detected[/bold yellow]")
            return

        for landmark in PoseLandmark:
            idx = landmark.value
            if idx < len(landmarks):
                point = landmarks[idx]
                osc_address_name = f"/pose/{landmark.name.lower()}"
                osc_address_index = f"/pose/{idx}"
                position = (point.x, point.y, point.z)

                # Log sending message
                console.log(f"📡 Sending: [cyan]{
                            osc_address_name}[/cyan] -> {position}")

                # Send OSC messages
                self.client.send_message(osc_address_name, position)
                self.client.send_message(osc_address_index, position)

    def send_specific_landmarks(self, landmarks, points_of_interest):
        """
        Send only specific landmarks via OSC.

        Args:
            landmarks: List of MediaPipe pose landmarks
            points_of_interest: List of PoseLandmark enums to track
        """
        if not landmarks:
            console.log("[bold yellow]⚠️ No landmarks detected[/bold yellow]")
            return

        for point in points_of_interest:
            idx = point.value
            if idx < len(landmarks):
                landmark = landmarks[idx]
                osc_address = f"/pose/{point.name.lower()}"
                position = (landmark.x, landmark.y, landmark.z)

                console.log(f"📡 Sending: [cyan]{
                            osc_address}[/cyan] -> {position}")
                self.client.send_message(osc_address, position)

    def close(self):
        """Close the OSC sender (if necessary)."""
        console.log("[bold red]🛑 OSC sender closed.[/bold red]")
