# Karel Snake: Manila Edition

### Final Project | Stanford University — Code in Place

An interactive 2D arcade reimagining of Stanford's classic **Karel the Robot**, built and submitted as the final capstone project for **Stanford University's Code in Place**.

> **Honors & Selection Context:**  
    > Developed as an admitted student in Stanford University's highly selective **Code in Place** program. Chosen as one of the few accepted participants out of **over 60,000 global applicants**, this project represents the culmination of intensive coursework covering software fundamentals, modular programming, algorithmic thinking, and user-driven software design.

---

##  Academic Concept & Philosophy

In Stanford's introductory Karel curriculum, students build foundational problem-solving skills by directing Karel to navigate orthogonal grids (avenues and streets) to manipulate beepers. 

**Karel Snake: Manila Edition** extends these static programming rules into a real-time, interactive arcade simulation themed after the traffic routes and intersections of Manila:
    - **Karel as the Locomotive Head:** Karel navigates city avenues and streets continuously, demanding real-time input decisions (`turn_left`, `turn_right`).
    - **Beepers as Passengers / Fares:** Each gold beeper collected grants points and appends a trailing passenger cabin behind Karel.
    - **City Boundaries & Roadblocks:** Standard Karel boundary collisions are integrated as failure states alongside dynamic road barricades that force quick path recalculations.

---

## Key Features

- **Dynamic Mega-Grid:** Starts on an expansive $25 \times 25$ street grid that dynamically expands (+2 width/height per level) as the game progresses.
- **Infinite Level Scaling:** 
  - Level 1 requires **10 beepers** to clear.
  - Every subsequent level scales up by +1 beeper (Level 2 = 11, Level 3 = 12, etc.).
  - Karel's transit step interval accelerates after every stage cleared.
- **Concrete Roadblocks:** Street barriers spawn starting at Level 2, introducing collision hazards that require proactive navigation.
- **Persistent High Scores:** Local Hall of Fame records the highest score locally in `highscore.txt`.
- **Game State Machine:** Smooth transitions between the Main Menu, High Scores board, active gameplay, and Game Over retry loops.

---

## Controls

### Menu Navigation
```
| Key | Action |
| :--- | :--- |
| `1` / `Enter` | Start Game |
| `2` / `H` | View High Scores |
| `Q` / `ESC` | Quit |
| `M` | Return to Main Menu |
```

### In-Game Navigation
```
| Key | Action |
| :--- | :--- |
| `A` / `Left Arrow` | Turn Karel Left (90°) |
| `D` / `Right Arrow` | Turn Karel Right (90°) |
| `ESC` | Exit to Main Menu |
| `R` | Quick Restart (on Game Over screen) |
```

---
## Project Structure

```
karel-goes-to-manila/
├── karel_snake.py         # Engine core: 2D grid rendering, level math, and obstacle tracking
├── play_karel_snake.py    # Game loop controller, event handling, and state machine
├── highscore.txt          # Persistent local score file
├── requirements.txt       # Dependencies (pygame-ce)
├── .gitignore             # Exclusion rules (caches and virtual environments)
└── README.md              # Project documentation and submission overview
```

### Installation & Execution
Clone the repository:

```
git clone [https://github.com/EngineerMapatac/karel-goes-to-manila.git](https://github.com/EngineerMapatac/karel-goes-to-manila.git)
cd karel-goes-to-manila
```

### Install dependencies:

```
pip install -r requirements.txt
```

### Run the game:

```
python3 play_karel_snake.py
```

## License & Attribution

Designed and developed by John Ramil Mapatac for the Stanford Code in Place program.

Distributed under the MIT License.