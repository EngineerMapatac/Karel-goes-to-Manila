# Karel Goes to Manila 🐶🏙️

An extended 2D simulation environment for Stanford's Code in Place. Watch Karel navigate traffic, manage dynamic battery resources, and handle urban delivery routing through the streets of Metro Manila in this infinite procedural grid game.

## Overview
This project extends the classic Karel the Robot into a custom terminal-based Endless Mode simulator. Built with Python, it models logistics routing, obstacle avoidance, resource management, and state persistence. 

As a 3rd-year Computer Engineering student transitioning into AI and Machine Learning, I structured this project as a foundational environment for autonomous agent logic—utilizing the same underlying grid-based architecture used to train AI pathfinding models.

### Core Features
* **Endless Mode & Procedural Generation:** The game generates infinite levels. As you progress, the grid size expands (up to 15x15) and traffic barriers increase to make pathfinding more complex.
* **8-Way Directional Movement:** The agent can move orthogonally and diagonally to optimize routes. Visual representation updates based on the current facing direction (🐶, 🐕, 🐩, 🐕‍🦺).
* **Dynamic Resource Management:** The battery limit automatically scales based on the map size and the number of packages to ensure the level remains achievable while still requiring efficiency.
* **Top 5 Leaderboard:** Utilizes Python File I/O (`highscore.txt`) to save and rank the top 5 players based on total score, tracking their highest level reached and fastest clearing speed.

## Controls
* `W` - Move North
* `S` - Move South
* `A` - Move West
* `D` - Move East
* `WA` / `WD` / `SA` / `SD` - Move Diagonally
* `Spacebar` (or `P`) - Pick up package
* `Q` - Quit the simulation

## Scoring System
The game heavily rewards routing efficiency and speed across multiple levels.
`Level Points = (Remaining Battery × 10) + Time Bonus`
*Time Bonus provides 10 extra points for every second under 30 seconds per level. Total Score accumulates as you clear levels.*


## How to Run
1. Ensure you have Python 3 installed.
2. Clone this repository to your local machine.
3. Open your terminal and navigate to the root directory.
4. Execute the main script:
   
```bash
   python src/main.py
```

## Repository Structure

```
karel-goes-to-manila/
├── src/
│   ├── main.py         # The core game loop, input handling, and rendering
│   └── map_data.py     # 2D list matrix defining the urban grid
└── README.md
``` 


## Acknowledgments
Developed as a capstone submission for Stanford University's Code in Place.