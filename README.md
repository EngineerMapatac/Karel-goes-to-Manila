# Karel Goes to Manila 3D 🇵🇭

A 3D interactive simulation inspired by Stanford's Karel the Robot, reimagined on the streets of Manila. 

This project uses a hybrid architecture:
- **Game Engine & Rendering:** Godot 4 (.NET/C#) handling 3D grid rendering, collision logic, and camera tracking.
- **Scripting & Control:** Python client sending real-time command instructions via local TCP sockets (`127.0.0.1:8080`).

---

## Architecture Overview

┌─────────────────────────────────┐        TCP Sockets         ┌─────────────────────────────────┐
│       Python Scripting          │     (Port 8080 / JSON)     │        Godot 4 3D Engine        │
│                                 │ ─────────────────────────> │                                 │
│  - move()                       │      "MOVE", "TURN_LEFT"   │  - KarelServer.cs               │
│  - turn_left()                  │ <───────────────────────── │  - 3D Grid & Collision checks   │
│  - pick_beeper() / put_beeper() │        "OK", "BLOCKED"     │  - Camera & transforms          │
└─────────────────────────────────┘                            └─────────────────────────────────┘

---

## Project Structure

Karel-goes-to-Manila/
├── Karel3D_Engine/          # Godot 4 .NET Project
│   ├── Scripts/
│   │   └── KarelServer.cs   # TCP Socket Server & Transform Controller
│   ├── MainScene.tscn       # 3D Grid, Camera, and Karel node
│   └── project.godot        # Engine configuration
└── Karel_Client/            # Python Client
    ├── karel3d.py           # Network driver & standard Karel API
    └── student_code.py      # Player algorithm / navigation code

---

## Prerequisites

* Godot 4 .NET / Mono Edition

* .NET 8.0 SDK

* Python 3.10+

---

## How to Run
1. Launch the Engine:

  * Open Karel3D_Engine in Godot 4.

  * Press F5 (or click Play) to launch MainScene.tscn.

  * The engine will start listening for socket connections on port 8080.

2. Run the Script:

  * Open a terminal in the root folder:

  ```
  python3 Karel_Client/student_code.py
  ```
  * Watch the 3D model execute turns and grid movements inside the Godot window.

---

## License

This project is licensed under the MIT License.