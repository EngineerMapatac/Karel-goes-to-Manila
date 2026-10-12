# Karel Snake: Manila Edition

An isometric, grid-based Snake game inspired by Stanford's Karel the Robot and set on the street intersections of Manila.

Built entirely with **Pure Python** and **Pygame**.

---

## Gameplay & Features

- **Isometric 2.5D Rendering:** Custom isometric projection drawn directly with Pygame polygon surfaces.
- **Classic Karel Rules:** Karel moves forward across the city grid, collecting golden beepers (passenger fares).
- **Snake Mechanics:** Every beeper collected lengthens Karel's passenger queue.
- **Fail Conditions:** Crashing into city boundaries or Karel's trailing cars ends the route.

---

## Controls

```
| Key | Action |
| :--- | :--- |
| `A` / `Left Arrow` | Turn Left (relative to Karel) |
| `D` / `Right Arrow` | Turn Right (relative to Karel) |
| `R` | Restart after crash |
| `ESC` / Close | Exit game |
```
---

## Installation & Setup

1. **Clone the repository:**
   ```
   git clone [https://github.com/EngineerMapatac/karel-goes-to-manila.git](https://github.com/EngineerMapatac/karel-goes-to-manila.git)
   cd karel-goes-to-manila
   ```

---
## Install dependencies:

    ```
    pip install -r requirements.txt
    ```

---
## Run the game:

    ```
    python3 play_karel_snake.py
    ```

---
## Project Structure

```
karel-goes-to-manila/
├── karel_snake.py         # Isometric rendering engine, grid math, and game state
├── play_karel_snake.py    # Game loop, user controls, and timer logic
├── requirements.txt       # Python dependencies (pygame)
└── README.md              # Project documentation
```

---
## License
This project is licensed under the MIT License.