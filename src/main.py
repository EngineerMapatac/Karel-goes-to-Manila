import os
import time
import random

# Robot State
robot = {
    "x": 1,
    "y": 1,
    "facing": "East",
    "packages": 0,
    "moves": 0,
    "battery": 40,
    "level": 1,
    "score": 0
}

def generate_level(level_num):
    # Randomize map size per level for more variety
    grid_size = random.randint(8, 12)
    new_grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    
    pkg_count = min(2 + level_num, 15)
    total_pkgs = 0
    while total_pkgs < pkg_count:
        rx, ry = random.randint(0, grid_size-1), random.randint(0, grid_size-1)
        if new_grid[ry][rx] == 0 and (rx != 1 or ry != 1):
            new_grid[ry][rx] = 2
            total_pkgs += 1
            
    barrier_count = min(3 + (level_num * 2), int((grid_size * grid_size) * 0.3))
    for _ in range(barrier_count):
        rx, ry = random.randint(0, grid_size-1), random.randint(0, grid_size-1)
        if new_grid[ry][rx] == 0 and (rx != 1 or ry != 1):
            new_grid[ry][rx] = 1
            
    return new_grid, total_pkgs

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_high_score():
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as file:
            data = file.read().strip().split(",")
            if len(data) >= 3:
                return data[0], int(data[1]), float(data[2])
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
    best_name, best_score, best_time = load_high_score()
    display_best_time = best_time if best_time != 999.99 else "--"
    
    # Display the high score champion prior to the beginning of the game
    print("========================================")
    print("   WELCOME TO KAREL GOES TO MANILA")
    print("            ENDLESS MODE")
    print("========================================")
    print(f"🏆 Current Champion: {best_name}")
    print(f"⭐ Highest Score: {best_score}")
    print(f"⚡ Fastest Level: {display_best_time}s")
    print("========================================\n")
    
    player_name = input("Enter your player name: ")
    
    manila_grid, total_packages = generate_level(robot["level"])
    level_start_time = time.time()
    playing = True
    
    while playing:
        current_time = round(time.time() - level_start_time, 2)
        clear_screen()
        
        print(f"Player: {player_name}  |  Total Score: {robot['score']}")
        print(f"Level: {robot['level']}  |  📦 Packages: {robot['packages']} / {total_packages}  |  🔋 Battery: {robot['battery']}  |  ⏱️ Time: {current_time}s\n")
        
        render_map(manila_grid, robot)
        
        if robot["packages"] == total_packages:
            time_taken = round(time.time() - level_start_time, 2)
            time_bonus = max(0, int((30 - time_taken) * 10))
            level_points = (robot["battery"] * 10) + time_bonus
            robot["score"] += level_points
            
            print(f"\nLevel {robot['level']} Cleared in {time_taken}s!")
            print(f"Points Earned: {level_points} (Total: {robot['score']})")
            
            if time_taken < best_time:
                print("⚡ NEW FASTEST LEVEL TIME! ⚡")
                best_time = time_taken
                save_high_score(best_name, best_score, best_time)
            
            time.sleep(2)
            
            robot["level"] += 1
            robot["battery"] += 20 
            robot["packages"] = 0
            robot["x"] = 1
            robot["y"] = 1
            manila_grid, total_packages = generate_level(robot["level"])
            level_start_time = time.time()
            continue
            
        if robot["battery"] <= 0:
            print(f"\nGame Over! The robot ran out of battery at Level {robot['level']}.")
            print(f"Final Score: {robot['score']}")
            
            if robot["score"] > best_score:
                print("🎉 NEW HIGH SCORE! 🎉")
                save_high_score(player_name, robot["score"], best_time)
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