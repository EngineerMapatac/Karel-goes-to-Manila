import pygame
import sys
import random
import os

SCREEN_W = 850
SCREEN_H = 800
HIGH_SCORE_FILE = "highscore.txt"

# Direction vectors: 0=East (+X), 1=North (-Y), 2=West (-X), 3=South (+Y)
DIRS = [(1, 0), (0, -1), (-1, 0), (0, 1)]

class KarelSnake2D:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Karel Snake: Manila Streets 2D (25x25)")
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 16, bold=True)
        self.title_font = pygame.font.SysFont("Arial", 38, bold=True)
        self.sub_font = pygame.font.SysFont("Arial", 20)

        self.state = "MENU"
        self.high_score = self.load_high_score()
        self.reset_full_game()

    def load_high_score(self):
        if os.path.exists(HIGH_SCORE_FILE):
            try:
                with open(HIGH_SCORE_FILE, "r") as f:
                    return int(f.read().strip())
            except Exception:
                return 0
        return 0

    def save_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            with open(HIGH_SCORE_FILE, "w") as f:
                f.write(str(self.high_score))

    def reset_full_game(self):
        self.level = 1
        self.score = 0
        self.init_level()

    def init_level(self):
        # Base map starts at 25x25 and expands by +2 every level
        self.grid_size = 25 + (self.level - 1) * 2
        
        # Scaling target: Level 1 = 10, Level 2 = 11, Level 3 = 12, etc.
        self.beepers_in_level = 0
        self.beepers_needed_to_level_up = 9 + self.level
        
        # Move delay dynamically tuned for large 25+ grids (min cap: 45ms)
        self.move_delay = max(45, 140 - (self.level - 1) * 10)

        # Dynamic tile size calculation to fit the screen
        margin_top = 70
        playable_w = SCREEN_W - 50
        playable_h = SCREEN_H - margin_top - 30
        self.tile_size = min(playable_w // self.grid_size, playable_h // self.grid_size)
        
        self.board_offset_x = (SCREEN_W - (self.grid_size * self.tile_size)) // 2
        self.board_offset_y = margin_top + (playable_h - (self.grid_size * self.tile_size)) // 2

        # Spawn Karel at center
        center = self.grid_size // 2
        self.body = [(center, center), (center - 1, center), (center - 2, center)]
        self.facing = 0  # Facing East

        # Spawn obstacles/walls (Level 1: 0, Level 2: 4, Level 3: 8, etc.)
        self.walls = set()
        num_walls = (self.level - 1) * 4
        while len(self.walls) < num_walls:
            wx = random.randint(0, self.grid_size - 1)
            wy = random.randint(0, self.grid_size - 1)
            # Avoid Karel's spawn lane
            if (wx, wy) not in self.body and abs(wy - center) > 2:
                self.walls.add((wx, wy))

        self.spawn_beeper()

    def spawn_beeper(self):
        while True:
            pos = (random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1))
            if pos not in self.body and pos not in self.walls:
                self.beeper = pos
                break

    def step(self, turn_command=None):
        if self.state != "PLAYING":
            return

        if turn_command == "LEFT":
            self.facing = (self.facing + 1) % 4
        elif turn_command == "RIGHT":
            self.facing = (self.facing - 1) % 4

        dx, dy = DIRS[self.facing]
        head_x, head_y = self.body[0]
        new_head = (head_x + dx, head_y + dy)

        # 1. Boundary collision
        if not (0 <= new_head[0] < self.grid_size and 0 <= new_head[1] < self.grid_size):
            self.handle_game_over()
            return

        # 2. Roadblock / Wall collision
        if new_head in self.walls:
            self.handle_game_over()
            return

        # 3. Self-body collision
        if new_head in self.body[:-1]:
            self.handle_game_over()
            return

        self.body.insert(0, new_head)

        # Check beeper pickup
        if new_head == self.beeper:
            self.score += 10 * self.level
            self.beepers_in_level += 1
            self.save_high_score()

            if self.beepers_in_level >= self.beepers_needed_to_level_up:
                self.level += 1
                self.init_level()
            else:
                self.spawn_beeper()
        else:
            self.body.pop()

    def handle_game_over(self):
        self.save_high_score()
        self.state = "GAME_OVER"

    def render(self):
        self.screen.fill((20, 24, 31))

        if self.state == "MENU":
            self.render_menu()
        elif self.state == "HIGH_SCORES":
            self.render_high_score_screen()
        elif self.state in ("PLAYING", "GAME_OVER"):
            self.render_gameplay()

        pygame.display.flip()

    def render_menu(self):
        title = self.title_font.render("KAREL GOES TO MANILA", True, (241, 196, 15))
        sub = self.sub_font.render("2D Mega Grid (25x25+)", True, (200, 200, 200))
        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 200))
        self.screen.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, 255))

        btn1 = self.sub_font.render("[ 1 ]  START GAME", True, (46, 204, 113))
        btn2 = self.sub_font.render("[ 2 ]  HIGH SCORES", True, (52, 152, 219))
        btn3 = self.sub_font.render("[ Q ]  QUIT", True, (231, 76, 60))

        self.screen.blit(btn1, (SCREEN_W // 2 - btn1.get_width() // 2, 380))
        self.screen.blit(btn2, (SCREEN_W // 2 - btn2.get_width() // 2, 440))
        self.screen.blit(btn3, (SCREEN_W // 2 - btn3.get_width() // 2, 500))

    def render_high_score_screen(self):
        title = self.title_font.render("MANILA HALL OF FAME", True, (241, 196, 15))
        score_val = self.title_font.render(f"High Score: {self.high_score}", True, (255, 255, 255))
        prompt = self.sub_font.render("Press [ M ] or [ ESC ] for Main Menu", True, (180, 180, 180))

        self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 240))
        self.screen.blit(score_val, (SCREEN_W // 2 - score_val.get_width() // 2, 340))
        self.screen.blit(prompt, (SCREEN_W // 2 - prompt.get_width() // 2, 460))

    def render_gameplay(self):
        # Header Info Bar
        rem = self.beepers_needed_to_level_up - self.beepers_in_level
        level_lbl = self.font.render(f"LEVEL: {self.level} (Grid: {self.grid_size}x{self.grid_size})", True, (46, 204, 113))
        score_lbl = self.font.render(f"SCORE: {self.score}", True, (255, 255, 255))
        high_lbl = self.font.render(f"BEST: {self.high_score}", True, (241, 196, 15))
        next_lbl = self.font.render(f"Next Level: {rem} beepers", True, (243, 156, 18))

        self.screen.blit(level_lbl, (self.board_offset_x, 15))
        self.screen.blit(score_lbl, (self.board_offset_x, 40))
        self.screen.blit(high_lbl, (SCREEN_W - self.board_offset_x - high_lbl.get_width(), 15))
        self.screen.blit(next_lbl, (SCREEN_W - self.board_offset_x - next_lbl.get_width(), 40))

        # Grid Background
        board_w = self.grid_size * self.tile_size
        board_h = self.grid_size * self.tile_size
        board_rect = pygame.Rect(self.board_offset_x, self.board_offset_y, board_w, board_h)
        pygame.draw.rect(self.screen, (32, 38, 48), board_rect)
        pygame.draw.rect(self.screen, (75, 85, 100), board_rect, 2)

        # Grid Lines
        for i in range(self.grid_size + 1):
            x = self.board_offset_x + i * self.tile_size
            pygame.draw.line(self.screen, (40, 48, 60), (x, self.board_offset_y), (x, self.board_offset_y + board_h), 1)
            y = self.board_offset_y + i * self.tile_size
            pygame.draw.line(self.screen, (40, 48, 60), (self.board_offset_x, y), (self.board_offset_x + board_w, y), 1)

        # Draw Obstacle Walls (Barricades)
        for (wx, wy) in self.walls:
            w_rect = pygame.Rect(
                self.board_offset_x + wx * self.tile_size + 1,
                self.board_offset_y + wy * self.tile_size + 1,
                self.tile_size - 2,
                self.tile_size - 2
            )
            pygame.draw.rect(self.screen, (100, 110, 125), w_rect)
            pygame.draw.rect(self.screen, (192, 57, 43), w_rect, 1)
            pygame.draw.line(self.screen, (192, 57, 43), (w_rect.left, w_rect.top), (w_rect.right, w_rect.bottom), 1)
            pygame.draw.line(self.screen, (192, 57, 43), (w_rect.left, w_rect.bottom), (w_rect.right, w_rect.top), 1)

        # Draw Golden Beeper
        bx = self.board_offset_x + self.beeper[0] * self.tile_size + self.tile_size // 2
        by = self.board_offset_y + self.beeper[1] * self.tile_size + self.tile_size // 2
        radius = max(3, self.tile_size // 3)
        pygame.draw.circle(self.screen, (241, 196, 15), (bx, by), radius)

        # Draw Karel's Head & Body
        for idx, (seg_x, seg_y) in enumerate(self.body):
            cell_rect = pygame.Rect(
                self.board_offset_x + seg_x * self.tile_size + 1,
                self.board_offset_y + seg_y * self.tile_size + 1,
                self.tile_size - 2,
                self.tile_size - 2
            )
            if idx == 0:
                pygame.draw.rect(self.screen, (231, 76, 60), cell_rect)
                dx, dy = DIRS[self.facing]
                dot_x = cell_rect.centerx + dx * (self.tile_size // 4)
                dot_y = cell_rect.centery + dy * (self.tile_size // 4)
                pygame.draw.circle(self.screen, (255, 255, 255), (dot_x, dot_y), max(2, self.tile_size // 6))
            else:
                pygame.draw.rect(self.screen, (52, 152, 219), cell_rect)

        # Game Over Screen
        if self.state == "GAME_OVER":
            overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 190))
            self.screen.blit(overlay, (0, 0))

            over_title = self.title_font.render("CRASHED ON EDSA!", True, (231, 76, 60))
            sub1 = self.sub_font.render("[ R ] Play Again", True, (255, 255, 255))
            sub2 = self.sub_font.render("[ M ] Main Menu", True, (200, 200, 200))

            self.screen.blit(over_title, (SCREEN_W // 2 - over_title.get_width() // 2, 300))
            self.screen.blit(sub1, (SCREEN_W // 2 - sub1.get_width() // 2, 380))
            self.screen.blit(sub2, (SCREEN_W // 2 - sub2.get_width() // 2, 430))