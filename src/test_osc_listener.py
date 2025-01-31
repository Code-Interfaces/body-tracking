from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer


def print_handler(address, *args):
    """Print received OSC messages."""
    print(f"Received OSC: {address} {args}")


dispatcher = Dispatcher()
dispatcher.map("/pose/*", print_handler)  # Listen to all pose messages

server = BlockingOSCUDPServer(("0.0.0.0", 8000), dispatcher)

print("Listening for OSC messages on port 8000...")
server.serve_forever()
