# Karel Goes to Manila 🐶🏙️

An extended 2D simulation environment for Stanford's Code in Place. Watch Karel navigate traffic, manage battery resources, and handle urban delivery routing through the streets of Metro Manila.

## Overview
This project extends the classic Karel the Robot into a custom terminal-based grid navigation simulator. Built with Python, it models logistics routing, obstacle avoidance, resource management, and state persistence. 

Beyond basic programming concepts, this project is structured as a foundational environment for autonomous agent logic—the same underlying grid-based architecture used to train Artificial Intelligence and Machine Learning (AI/ML) pathfinding models.

## Core Features
* **Agent State Management:** Tracks dynamic X/Y coordinates, facing direction, inventory, and battery life using Python dictionaries.
* **2D Grid Architecture:** Utilizes nested lists (matrices) to render the environment, traffic barriers (`🚧`), and delivery packages (`📦`).
* **Resource Optimization (Battery Limit):** Implements a movement constraint. The agent must find the most efficient path to deliver all packages before the battery drains.
* **Persistent High Scores:** Utilizes Python File I/O (`highscore.txt`) to save player names and highest efficiency scores across sessions.
* **Directional Rendering:** Updates the agent's visual representation (🐶, 🐕, 🐩, 🐕‍🦺) based on the current movement direction.

## Controls
* `W` - Move Up (North)
* `S` - Move Down (South)
* `A` - Move Left (West)
* `D` - Move Right (East)
* `Spacebar` (or `P`) - Pick up package
* `Q` - Quit the simulation

## Scoring System
The game rewards routing efficiency. Taking the shortest path uses less battery.
`Final Score = Remaining Battery × 100`

## Scoring System
The game rewards routing efficiency and speed. Taking the shortest path uses less battery, and finishing quickly grants bonus points.
`Final Score = (Remaining Battery × 100) + Time Bonus`
*Time Bonus provides 10 extra points for every second under 30 seconds.*

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