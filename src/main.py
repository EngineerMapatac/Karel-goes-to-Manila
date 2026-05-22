import os
import time
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
            # Check if the file has the new time format
            if len(data) >= 3:
                return data[0], int(data[1]), float(data[2])
            # Fallback for the old format without time
            elif len(data) == 2:
                return data[0], int(data[1]), 999.99
    return "No one", 0, 999.99

def save_high_score(name, score, time_taken):
    with open("highscore.txt", "w") as file:
        file.write(f"{name},{score},{time_taken}")

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
    best_name, best_score, best_time = load_high_score()
    
    start_time = time.time()
    playing = True
    
    while playing:
        current_time = round(time.time() - start_time, 2)
        clear_screen()
        
        display_best_time = best_time if best_time != 999.99 else "--"
        
        print(f"Player: {player_name}  |  High Score: {best_score} ({best_name})  |  Fastest: {display_best_time}s")
        print(f"📦 Packages: {robot['packages']} / {total_packages}  |  🔋 Battery: {robot['battery']}  |  ⏱️ Time: {current_time}s\n")
        
        render_map(manila_grid, robot)
        
        if robot["packages"] == total_packages:
            time_taken = round(time.time() - start_time, 2)
            # Add a time bonus: 10 extra points for every second under 30 seconds
            time_bonus = max(0, int((30 - time_taken) * 10))
            final_score = (robot["battery"] * 100) + time_bonus
            
            print(f"\nCongratulations {player_name}! You delivered all packages!")
            print(f"Time Taken: {time_taken}s")
            print(f"Base Score: {robot['battery'] * 100} + Time Bonus: {time_bonus}")
            print(f"Total Score: {final_score}")
            
            new_record = False
            if final_score > best_score:
                print("🎉 NEW HIGH SCORE! 🎉")
                best_score = final_score
                new_record = True
                
            if time_taken < best_time:
                print("⚡ NEW FASTEST TIME! ⚡")
                best_time = time_taken
                new_record = True
                
            if new_record:
                save_high_score(player_name, best_score, best_time)
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