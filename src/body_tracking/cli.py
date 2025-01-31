from .osc_server import OSCSender
from .tracking import BodyTracker
from .config import config
from rich.console import Console
from rich.progress import Progress
import cv2
import click
import os

# Suppress TensorFlow Lite verbose logs
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

# Initialize Rich Console
console = Console()


@click.command()
@click.option("--host", default=config.SERVER_IP, help="OSC server host.")
@click.option("--port", default=config.SERVER_PORT, help="OSC server port.")
@click.option("-D", "--debug", is_flag=True, help="Enable debug mode (show video with landmarks).")
def main(host, port, debug):
    """Run the body tracking CLI and send OSC data."""
    tracker = BodyTracker()
    osc = OSCSender(host, port)
    cap = cv2.VideoCapture(0)  # Open webcam

    console.print(
        f"[bold green]🚀 Tracking started[/bold green] (Press 'q' to quit)")
    console.print(f"📡 Sending OSC data to [bold blue]{
                  host}:{port}[/bold blue]")

    with Progress() as progress:
        tracking_task = progress.add_task("[cyan]Tracking...", total=None)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                console.log(
                    "[bold yellow]⚠️ Ignoring empty camera frame[/bold yellow]")
                continue

            frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
            frame.flags.writeable = False
            landmarks = tracker.track(frame)
            frame.flags.writeable = True
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            if landmarks and landmarks.pose_landmarks:
                osc.send_landmarks(landmarks.pose_landmarks.landmark)
                console.log("[green]✅ Landmarks sent[/green]")

                # Draw landmarks only if debug mode is enabled
                if debug:
                    tracker.mp_drawing.draw_landmarks(
                        frame, landmarks.pose_landmarks, tracker.mp_pose.POSE_CONNECTIONS)

            # Show the tracking window only in debug mode
            if debug:
                cv2.imshow("Tracking", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        progress.remove_task(tracking_task)

    cap.release()
    cv2.destroyAllWindows()
    tracker.close()

    console.print("[bold red]🛑 Tracking stopped.[/bold red]")


if __name__ == "__main__":
    main()
