import socket
import sys

class _KarelSocketClient:
    def __init__(self, host="127.0.0.1", port=8080):
        self.host = host
        self.port = port
        self.sock = None

    def connect(self):
        if not self.sock:
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((self.host, self.port))
            except ConnectionRefusedError:
                print("\n[Error] Could not connect to Godot Karel 3D!")
                print("Make sure your Godot game is currently running (Play / F5) before executing this script.\n")
                sys.exit(1)

    def send_command(self, cmd: str) -> str:
        self.connect()
        self.sock.sendall((cmd + "\n").encode("utf-8"))
        response = self.sock.recv(1024).decode("utf-8").strip()
        return response

_client = _KarelSocketClient()

def move():
    """Moves Karel 1 block forward in the facing direction."""
    res = _client.send_command("MOVE")
    if res == "BLOCKED":
        raise RuntimeError("Front is blocked! Karel hit an obstacle or the city boundary.")

def turn_left():
    """Turns Karel 90 degrees counter-clockwise."""
    _client.send_command("TURN_LEFT")

def pick_beeper():
    """Picks up a beeper/coin at Karel's current intersection."""
    res = _client.send_command("PICK")
    if res == "NO_BEEPER":
        raise RuntimeError("No beeper present on this tile!")

def put_beeper():
    """Places a beeper/coin on Karel's current intersection."""
    _client.send_command("PUT")