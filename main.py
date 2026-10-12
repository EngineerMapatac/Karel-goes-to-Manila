import math
import time
from ursina import *

app = Ursina(title="Karel Goes to Manila - 3D")

# --- Grid Configuration ---
GRID_WIDTH = 10
GRID_HEIGHT = 10

# Ground Plane
ground = Entity(
    model='plane',
    scale=(GRID_WIDTH, 1, GRID_HEIGHT),
    color=color.rgb(35, 35, 40),
    position=(GRID_WIDTH / 2 - 0.5, 0, GRID_HEIGHT / 2 - 0.5)
)

# Street Grid Lines
for x in range(GRID_WIDTH):
    for z in range(GRID_HEIGHT):
        Entity(
            model='quad',
            rotation_x=90,
            scale=0.92,
            color=color.rgb(55, 55, 60),
            position=(x, 0.01, z)
        )

# --- Karel / Jeepney Setup ---
# Update paths to match your assets folder:
# e.g., 'assets/jeepney.obj' or 'assets/jeepney.glb'
karel = Entity(
    model='assets/jeepney.obj',             # or 'cube' if testing before adding the file
    texture='assets/jeepney_texture.png',   # omit if using .glb or untextured .obj
    scale=0.5,                              # scale to fit inside 1 grid tile
    position=(0, 0.05, 0),
    rotation_y=0                            # change to 90, 180, or 270 if it doesn't face North
)

# Coordinate & Direction State
# Directions: 0 = East (+X), 1 = North (+Z), 2 = West (-X), 3 = South (-Z)
karel_grid_x = 0
karel_grid_z = 0
facing_direction = 1
DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

# --- Obstacles (Roadblocks) ---
barriers = [(3, 3), (3, 4), (5, 2), (7, 6)]
for bx, bz in barriers:
    Entity(
        model='cube',
        color=color.orange,
        scale=(0.7, 0.7, 0.7),
        position=(bx, 0.35, bz)
    )

# --- Beepers / Manila Coins ---
beepers = {}
beeper_coords = [(1, 4), (4, 5), (6, 2), (8, 8)]
for bx, bz in beeper_coords:
    beepers[(bx, bz)] = Entity(
        model='sphere',
        color=color.gold,
        scale=0.35,
        position=(bx, 0.35, bz)
    )

# --- Camera Setup ---
camera.position = (GRID_WIDTH / 2, 13, -5)
camera.rotation_x = 52
camera.fov = 50

# --- Core Karel Mechanics ---
def turn_left():
    global facing_direction
    facing_direction = (facing_direction + 1) % 4
    karel.animate_rotation_y(karel.rotation_y - 90, duration=0.12)

def move_forward():
    global karel_grid_x, karel_grid_z
    dx, dz = DIRECTIONS[facing_direction]
    next_x = karel_grid_x + dx
    next_z = karel_grid_z + dz

    # City border bounds check
    if not (0 <= next_x < GRID_WIDTH and 0 <= next_z < GRID_HEIGHT):
        print("Cannot move: City border reached!")
        return

    # Roadblock collision check
    if (next_x, next_z) in barriers:
        print("Cannot move: Obstacle ahead!")
        return

    karel_grid_x = next_x
    karel_grid_z = next_z
    karel.animate_position((karel_grid_x, 0.05, karel_grid_z), duration=0.15)

def pick_beeper():
    pos = (karel_grid_x, karel_grid_z)
    if pos in beepers:
        destroy(beepers[pos])
        del beepers[pos]
        print("Beeper picked up!")

# --- Input & Loop ---
def input(key):
    if key in ('w', 'up arrow'):
        move_forward()
    elif key in ('a', 'left arrow'):
        turn_left()
    elif key == 'space':
        pick_beeper()

def update():
    # Subtle idle rumble
    karel.y = 0.05 + (math.sin(time.time() * 20) * 0.008)

app.run()