##Karel Goes to Manila 3D##
---

A 3D adaptation of the Stanford Code in Place Karel project. Rebuilt with Python and the Ursina Engine, this game translates traditional discrete grid logic into an interactive 3D simulation through the streets of Manila.

Navigate traffic, avoid urban roadblocks, collect tokens, and drive through the city grid.

---

**Features**

* 3D Grid System: Classic Karel grid coordinates mapped directly into 3D world space.
* Custom Jeepney Model: Support for textured .obj and .glb vehicle models with dynamic engine idling.
* Obstacle Navigation: Collision handling for Manila traffic barriers and city boundary limits.
* Collection Mechanics: Interactive coin/beeper collection with state updates.
* Smooth Animations: Interpolated rotations and movement transitions between intersections.

---

#Project Structure

```
karel-goes-to-manila/
├── assets/
│   ├── jeepney.obj          # 3D player model (or .glb)
│   └── jeepney_texture.png  # Model texture map
├── .gitignore
├── main.py                  # Game loop, logic, and Ursina scene setup
├── README.md
└── requirements.txt

```

Installation & Setup1. Clone the RepositoryBashgit clone https://github.com/EngineerMapatac/Karel-goes-to-Manila.git
cd Karel-goes-to-Manila
2. Set Up a Virtual EnvironmentmacOS / Linux:Bashpython3 -m venv venv
source venv/bin/activate
Windows:Bashpython -m venv venv
venv\Scripts\activate
3. Install DependenciesBashpip install -r requirements.txt
(Or install Ursina directly: pip install ursina)Running the GameLaunch the game by executing the entry point:Bashpython main.py
ControlsKeyActionIn-Game MechanicW / Up ArrowMove ForwardMoves 1 block forward in the facing direction (move())A / Left ArrowTurn LeftRotates 90° counter-clockwise (turn_left())SpacebarPick BeeperCollects a coin/beeper at the current intersectionEscapeQuitCloses the game windowRequirementsPython 3.8+Ursina Engine (pip install ursina)OpenGL-compatible graphics driverLicenseThis project is licensed under the MIT License — see the LICENSE file for details.
