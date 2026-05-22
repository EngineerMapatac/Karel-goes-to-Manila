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
    "battery": 0,
    "level": 1,
    "score": 0
}

def generate_level(level_num):
    grid_size = min(8 + (level_num // 2), 15)
    new_grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    
    pkg_count = min(2 + (level_num // 3), 8)
    total_pkgs = 0
    while total_pkgs < pkg_count:
        rx, ry = random.randint(0, grid_size-1), random.randint(0, grid_size-1)
        if new_grid[ry][rx] == 0 and (rx != 1 or ry != 1):
            new_grid[ry][rx] = 2
            total_pkgs += 1
            
    barrier_count = min(5 + (level_num * 3), int((grid_size * grid_size) * 0.4))
    for _ in range(barrier_count):
        rx, ry = random.randint(0, grid_size-1), random.randint(0, grid_size-1)
        if new_grid[ry][rx] == 0 and (rx != 1 or ry != 1):
            new_grid[ry][rx] = 1
            
    # Dynamic battery calculation based on difficulty
    level_battery = 30 + (grid_size * 2) + (total_pkgs * 5)
            
    return new_grid, total_pkgs, level_battery

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_high_scores():
    scores = []
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as file:
            for line in file:
                data = line.strip().split(",")
                if len(data) == 4:
                    scores.append((data[0], int(data[1]), int(data[2]), float(data[3])))
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:5]

def check_and_save_score(name, score, level, time_taken):
    scores = load_high_scores()
    scores.append((name, score, level, time_taken))
    scores.sort(key=lambda x: x[1], reverse=True)
    scores = scores[:5]
    
    with open("highscore.txt", "w") as file:
        for item in scores:
            file.write(f"{item[0]},{item[1]},{item[2]},{item[3]}\n")

def render_map(grid, bot):
    icons = {
        "North": " 🐕 ", "South": " 🐕‍🦺", "East": " 🐩 ", "West": " 🐶 ",
        "North-East": " 🐩 ", "North-West": " 🐶 ", 
        "South-East": " 🐕‍🦺", "South-West": " 🐕 "
    }
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
    high_scores = load_high_scores()
    
    print("====================================================")
    print("         WELCOME TO KAREL GOES TO MANILA")
    print("                  ENDLESS MODE")
    print("====================================================")
    print("🏆 TOP 5 LEADERBOARD:")
    print(f"{'Rank':<5} {'Player':<15} {'Score':<10} {'Level':<8} {'Speed':<8}")
    print("-" * 52)
    
    if not high_scores:
        print("No records yet! Be the first one to set a score.")
    else:
        for i, (name, score, lvl, t_taken) in enumerate(high_scores, 1):
            print(f"{i:<5} {name:<15} {score:<10} {lvl:<8} {t_taken}s")
            
    print("====================================================\n")
    
    player_name = input("Enter your player name: ")
    
    manila_grid, total_packages, current_max_battery = generate_level(robot["level"])
    robot["battery"] = current_max_battery
    level_start_time = time.time()
    playing = True
    
    fastest_level_time = 999.99
    
    while playing:
        current_time = round(time.time() - level_start_time, 2)
        clear_screen()
        
        top_score_display = high_scores[0][1] if high_scores else 0
        
        print(f"Player: {player_name}  |  Current Score: {robot['score']}  |  Target High Score: {top_score_display}")
        print(f"Level: {robot['level']}  |  📦 Packages: {robot['packages']} / {total_packages}  |  🔋 Battery: {robot['battery']} / {current_max_battery}  |  ⏱️ Time: {current_time}s\n")
        
        render_map(manila_grid, robot)
        
        if robot["packages"] == total_packages:
            time_taken = round(time.time() - level_start_time, 2)
            time_bonus = max(0, int((30 - time_taken) * 10))
            level_points = (robot["battery"] * 10) + time_bonus
            robot["score"] += level_points
            
            if time_taken < fastest_level_time:
                fastest_level_time = time_taken
            
            print(f"\nLevel {robot['level']} Cleared in {time_taken}s!")
            print(f"Points Earned: {level_points} (Total: {robot['score']})")
            time.sleep(2)
            
            robot["level"] += 1
            robot["packages"] = 0
            robot["x"] = 1
            robot["y"] = 1
            manila_grid, total_packages, current_max_battery = generate_level(robot["level"])
            robot["battery"] = current_max_battery
            level_start_time = time.time()
            continue
            
        if robot["battery"] <= 0:
            print(f"\nGame Over! The robot ran out of battery at Level {robot['level']}.")
            print(f"Final Score: {robot['score']}")
            
            final_fastest = fastest_level_time if fastest_level_time != 999.99 else current_time
            check_and_save_score(player_name, robot["score"], robot["level"], final_fastest)
            break
            
        print("\nCommands: [w] Up | [s] Down | [a] Left | [d] Right | [wa/wd/sa/sd] Diagonals | [space] Pick | [q] Quit")
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

        elif action in ['wa', 'aw']: 
            robot["facing"] = "North-West"
            if robot["y"] > 0 and robot["x"] > 0 and manila_grid[robot["y"] - 1][robot["x"] - 1] != 1:
                robot["y"] -= 1
                robot["x"] -= 1
                robot["moves"] += 1
                robot["battery"] -= 1

        elif action in ['wd', 'dw']: 
            robot["facing"] = "North-East"
            if robot["y"] > 0 and robot["x"] < len(manila_grid[0]) - 1 and manila_grid[robot["y"] - 1][robot["x"] + 1] != 1:
                robot["y"] -= 1
                robot["x"] += 1
                robot["moves"] += 1
                robot["battery"] -= 1

        elif action in ['sa', 'as']: 
            robot["facing"] = "South-West"
            if robot["y"] < len(manila_grid) - 1 and robot["x"] > 0 and manila_grid[robot["y"] + 1][robot["x"] - 1] != 1:
                robot["y"] += 1
                robot["x"] -= 1
                robot["moves"] += 1
                robot["battery"] -= 1

        elif action in ['sd', 'ds']: 
            robot["facing"] = "South-East"
            if robot["y"] < len(manila_grid) - 1 and robot["x"] < len(manila_grid[0]) - 1 and manila_grid[robot["y"] + 1][robot["x"] + 1] != 1:
                robot["y"] += 1
                robot["x"] += 1
                robot["moves"] += 1
                robot["battery"] -= 1
                
        elif action == ' ' or action == 'p' or action == '': 
            if manila_grid[robot["y"]][robot["x"]] == 2:
                manila_grid[robot["y"]][robot["x"]] = 0
                robot["packages"] += 1

if __name__ == "__main__":
    main()