import os
from map_data import manila_grid

# Robot State with directional facing
robot = {
    "x": 1,
    "y": 1,
    "facing": "East",
    "packages": 0,
    "moves": 0
}

total_packages = 0
for row in manila_grid:
    for cell in row:
        if cell == 2:
            total_packages += 1

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def render_map(grid, bot):
    # Emojis represent Karel facing North, South, East, West
    icons = {"North": " 🐕 ", "South": " 🐕‍🦺", "East": " 🐩 ", "West": " 🐶 "}
    
    for row_index in range(len(grid)):
        row_string = ""
        for col_index in range(len(grid[row_index])):
            if col_index == bot["x"] and row_index == bot["y"]:
                row_string += icons[bot["facing"]]
            else:
                cell = grid[row_index][col_index]
                if cell == 0:
                    row_string += " .  "
                elif cell == 1:
                    row_string += " 🚧 "
                elif cell == 2:
                    row_string += " 📦 "
        print(row_string)

def main():
    playing = True
    
    while playing:
        clear_screen()
        print(f"📦 Packages: {robot['packages']} / {total_packages}  |  👣 Moves: {robot['moves']}  |  🧭 Facing: {robot['facing']}\n")
        
        render_map(manila_grid, robot)
        
        if robot["packages"] == total_packages:
            print(f"\nCongratulations! You delivered all packages across Metro Manila in {robot['moves']} moves!")
            break
            
        print("\nCommands: [m] Move Forward | [l] Turn Left | [p] Pick Package | [d] Drop Package | [q] Quit")
        action = input("Enter command: ").lower()
        
        if action == 'q':
            playing = False
            print("Shutting down robot. Goodbye!")
            
        # Core Karel feature: Turn Left
        elif action == 'l': 
            directions = ["North", "West", "South", "East"]
            current_idx = directions.index(robot["facing"])
            robot["facing"] = directions[(current_idx + 1) % 4]
            robot["moves"] += 1
            
        # Core Karel feature: Move Forward based on facing direction
        elif action == 'm': 
            next_x = robot["x"]
            next_y = robot["y"]
            
            if robot["facing"] == "North": 
                next_y -= 1
            elif robot["facing"] == "South": 
                next_y += 1
            elif robot["facing"] == "East": 
                next_x += 1
            elif robot["facing"] == "West": 
                next_x -= 1
            
            # Boundary and wall collision check
            if 0 <= next_y < len(manila_grid) and 0 <= next_x < len(manila_grid[0]):
                if manila_grid[next_y][next_x] != 1:
                    robot["x"] = next_x
                    robot["y"] = next_y
                    robot["moves"] += 1
                    
        # Core Karel feature: Pick Beeper (Package)
        elif action == 'p': 
            if manila_grid[robot["y"]][robot["x"]] == 2:
                manila_grid[robot["y"]][robot["x"]] = 0
                robot["packages"] += 1
                
        # Core Karel feature: Put Beeper (Drop Package)
        elif action == 'd': 
            if robot["packages"] > 0 and manila_grid[robot["y"]][robot["x"]] == 0:
                manila_grid[robot["y"]][robot["x"]] = 2
                robot["packages"] -= 1

if __name__ == "__main__":
    main()