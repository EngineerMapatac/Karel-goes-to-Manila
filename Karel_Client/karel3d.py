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
                print("Error: Could not connect to the C# Karel 3D game!")
                print("Ensure the C# / Godot game is running first.")
                sys.exit(1)

    def send_command(self, cmd: str) -> str:
        self.connect()
        self.sock.sendall((cmd + "\n").encode("utf-8"))
        response = self.sock.recv(1024).decode("utf-8").strip()
        return response

_client = _KarelSocketClient()

def move():
    res = _client.send_command("MOVE")
    if res == "BLOCKED":
        raise RuntimeError("Collision: Karel cannot move forward!")

def turn_left():
    _client.send_command("TURN_LEFT")

def pick_beeper():
    res = _client.send_command("PICK")
    if res == "NO_BEEPER":
        raise RuntimeError("No beeper present on this tile!")

def put_beeper():
    _client.send_command("PUT")