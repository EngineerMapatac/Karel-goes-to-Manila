# Karel Goes to Manila

An extended 2D simulation environment for Stanford's Code in Place. Watch Karel navigate traffic and handle urban delivery routing through the streets of Manila.

## Overview
This project extends the classic Karel the Robot into a custom terminal-based grid navigation simulator. Built with Python, it models logistics routing, obstacle avoidance, and spatial state management. 

Beyond basic programming concepts, this project is structured as a foundational environment for autonomous agent logic—the same underlying grid-based architecture used to train early Artificial Intelligence and Machine Learning (AI/ML) pathfinding models.

## Core Features
* **Agent State Management:** Tracks the robot's dynamic X/Y coordinates, facing direction, and inventory using Python dictionaries.
* **2D Grid Architecture:** Utilizes nested lists (matrices) to render the environment, traffic barriers (`🚧`), and delivery packages (`📦`).
* **Collision Detection Engine:** Prevents the agent from moving out-of-bounds and enforces strict barrier logic for solid objects.
* **Dynamic Terminal Rendering:** Employs nested loop-based rendering to seamlessly update the UI state upon user input.

## Repository Structure

```
karel-goes-to-manila/
├── src/
│   ├── main.py         # The core game loop, input handling, and rendering
│   └── map_data.py     # 2D list matrix defining the urban grid
└── README.md
```

## How to Run
Ensure you have Python 3 installed.

Clone this repository to your local machine.

Navigate to the src directory in your terminal.

Execute the main script:

```
Bash
   python main.py
```

Use the W, A, S, D keys to navigate the grid, P to pick up a package, and Q to quit.


## Acknowledgments
Developed as a capstone submission for Stanford University's Code in Place.