import os
from map_data import manila_grid

# Robot State
robot = {
    "x": 1,
    "y": 1,
    "facing": "East",
    "packages": 0,
    "moves": 0,
    "battery": 40
}

# Calculate total packages
total_packages = 0
for row in manila_grid:
    for cell in row:
        if cell == 2:
            total_packages += 1

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_high_score():
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as file:
            data = file.read().strip().split(",")
            if len(data) == 2:
                return data[0], int(data[1])
    return "No one", 0

def save_high_score(name, score):
    with open("highscore.txt", "w") as file:
        file.write(f"{name},{score}")

def render_map(grid, bot):
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
    clear_screen()
    print("Welcome to Karel Goes to Manila!")
    player_name = input("Enter your player name: ")
    best_name, best_score = load_high_score()
    
    playing = True
    
    while playing:
        clear_screen()
        print(f"Player: {player_name}  |  High Score: {best_score} ({best_name})")
        print(f"📦 Packages: {robot['packages']} / {total_packages}  |  🔋 Battery: {robot['battery']}  |  👣 Moves: {robot['moves']}\n")
        
        render_map(manila_grid, robot)
        
        if robot["packages"] == total_packages:
            final_score = robot["battery"] * 100
            print(f"\nCongratulations {player_name}! You delivered all packages!")
            print(f"Your Score: {final_score}")
            
            if final_score > best_score:
                print("🎉 NEW HIGH SCORE! 🎉")
                save_high_score(player_name, final_score)
            break
            
        if robot["battery"] <= 0:
            print("\nGame Over! The robot ran out of battery.")
            break
            
        print("\nCommands: [w] Up | [s] Down | [a] Left | [d] Right | [spacebar] Pick Package | [q] Quit")
        action = input("Enter command: ").lower()
        
        if action == 'q':
            playing = False
            print("Shutting down robot. Goodbye!")
            
        elif action == 'w': 
            robot["facing"] = "North"
            if robot["y"] > 0 and manila_grid[robot["y"] - 1][robot["x"]] != 1:
                robot["y"] -= 1
                robot["moves"] += 1
                robot["battery"] -= 1
                
        elif action == 's': 
            robot["facing"] = "South"
            if robot["y"] < len(manila_grid) - 1 and manila_grid[robot["y"] + 1][robot["x"]] != 1:
                robot["y"] += 1
                robot["moves"] += 1
                robot["battery"] -= 1
                
        elif action == 'a': 
            robot["facing"] = "West"
            if robot["x"] > 0 and manila_grid[robot["y"]][robot["x"] - 1] != 1:
                robot["x"] -= 1
                robot["moves"] += 1
                robot["battery"] -= 1
                
        elif action == 'd': 
            robot["facing"] = "East"
            if robot["x"] < len(manila_grid[0]) - 1 and manila_grid[robot["y"]][robot["x"] + 1] != 1:
                robot["x"] += 1
                robot["moves"] += 1
                robot["battery"] -= 1
                
        elif action == ' ' or action == 'p' or action == '': 
            if manila_grid[robot["y"]][robot["x"]] == 2:
                manila_grid[robot["y"]][robot["x"]] = 0
                robot["packages"] += 1

if __name__ == "__main__":
    main()