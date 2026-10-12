Karel Goes to Manila 3D
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

Project Structure
---
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
---

Installation & Setup
---

---

1. Clone the Repository
```
git clone https://github.com/EngineerMapatac/Karel-goes-to-Manila.git
cd Karel-goes-to-Manila
```

2. Set Up a Virtual Environment

  macOS / Linux:

```
python3 -m venv venv
source venv/bin/activate
```

  Windows:

```
python -m venv venv
venv\Scripts\activate

```

3. Install Dependencies

```
pip install -r requirements.txt

```
(Or install Ursina directly: pip install ursina)

Running the Game
  Launch the game by executing the entry point:
  
```
python main.py
```
---

License
---
This project is licensed under the MIT License — see the LICENSE file for details.
