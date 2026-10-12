import pygame
import random
import os

GRID_COUNT = 25
CELL_SIZE = 32
W = GRID_COUNT * CELL_SIZE  # 800 x 800 window
HIGH_SCORE_FILE = "highscore.txt"

class KarelSnakeGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Karel Snake: Manila Streets (25x25)")
        self.screen = pygame.display.set_mode((W, W))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 18, bold=True)
        self.title_font = pygame.font.SysFont("Arial", 36, bold=True)
        
        self.high_score = self.load_high_score()
        self.reset_game()

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

    def reset_game(self):
        center = (GRID_COUNT // 2) * CELL_SIZE
        self.snake = [[center, center], [center - CELL_SIZE, center], [center - 2 * CELL_SIZE, center]]
        self.direction = (CELL_SIZE, 0)
        self.score = 0
        self.level = 1
        self.beepers_in_level = 0
        self.fps = 10
        self.walls = set()
        self.game_over = False
        self.spawn_beeper()

    def spawn_beeper(self):
        while True:
            pos = [random.randrange(0, W, CELL_SIZE), random.randrange(0, W, CELL_SIZE)]
            if pos not in self.snake and tuple(pos) not in self.walls:
                self.beeper = pos
                break

    def spawn_walls(self):
        num_walls = (self.level - 1) * 3
        while len(self.walls) < num_walls:
            wx = random.randrange(0, W, CELL_SIZE)
            wy = random.randrange(0, W, CELL_SIZE)
            if [wx, wy] not in self.snake and [wx, wy] != self.beeper:
                self.walls.add((wx, wy))

    def step(self):
        if self.game_over:
            return

        head = [self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1]]
        self.snake.insert(0, head)

        # Collision with Boundary, Self, or Concrete Roadblocks
        if (head[0] < 0 or head[0] >= W or 
            head[1] < 0 or head[1] >= W or 
            head in self.snake[1:] or 
            tuple(head) in self.walls):
            self.game_over = True
            self.save_high_score()
            return

        # Beeper collected
        if head == self.beeper:
            self.score += 10 * self.level
            self.beepers_in_level += 1
            self.save_high_score()

            # Level progression rule: 9 + Level beepers
            if self.beepers_in_level >= (9 + self.level):
                self.level += 1
                self.beepers_in_level = 0
                self.fps = min(22, self.fps + 1)
                self.spawn_walls()

            self.spawn_beeper()
        else:
            self.snake.pop()

    def render(self):
        self.screen.fill((22, 27, 34))

        # 1. Manila Road Grid lines
        for x in range(0, W, CELL_SIZE):
            pygame.draw.line(self.screen, (35, 42, 54), (x, 0), (x, W), 1)
        for y in range(0, W, CELL_SIZE):
            pygame.draw.line(self.screen, (35, 42, 54), (0, y), (W, y), 1)

        # 2. Roadblocks / Barricades
        for wx, wy in self.walls:
            rect = pygame.Rect(wx + 2, wy + 2, CELL_SIZE - 4, CELL_SIZE - 4)
            pygame.draw.rect(self.screen, (108, 122, 137), rect, border_radius=3)
            pygame.draw.line(self.screen, (192, 57, 43), (rect.left, rect.top), (rect.right, rect.bottom), 2)
            pygame.draw.line(self.screen, (192, 57, 43), (rect.left, rect.bottom), (rect.right, rect.top), 2)

        # 3. Golden Beeper
        bx = self.beeper[0] + CELL_SIZE // 2
        by = self.beeper[1] + CELL_SIZE // 2
        pygame.draw.circle(self.screen, (241, 196, 15), (bx, by), CELL_SIZE // 3)

        # 4. Karel (Red Head) and Trailing Cars (Cyan Body)
        for i, s in enumerate(self.snake):
            color = (231, 76, 60) if i == 0 else (52, 152, 219)
            rect = pygame.Rect(s[0] + 1, s[1] + 1, CELL_SIZE - 2, CELL_SIZE - 2)
            pygame.draw.rect(self.screen, color, rect, border_radius=4 if i == 0 else 2)

        # 5. Top UI Bar
        hud = self.font.render(f"LEVEL: {self.level}  |  SCORE: {self.score}  |  BEST: {self.high_score}", True, (240, 240, 240))
        self.screen.blit(hud, (15, 12))

        # 6. Game Over Overlay
        if self.game_over:
            overlay = pygame.Surface((W, W), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))
            msg = self.title_font.render("CRASHED ON EDSA!", True, (231, 76, 60))
            sub = self.font.render("Press [ R ] to Restart", True, (255, 255, 255))
            self.screen.blit(msg, (W // 2 - msg.get_width() // 2, W // 2 - 30))
            self.screen.blit(sub, (W // 2 - sub.get_width() // 2, W // 2 + 25))

        pygame.display.flip()

def main():
    game = KarelSnakeGame()
    running = True

    while running:
        game.clock.tick(game.fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Cardinal directional controls (prevent 180 reversal)
                if event.key in (pygame.K_UP, pygame.K_w) and game.direction != (0, CELL_SIZE):
                    game.direction = (0, -CELL_SIZE)
                elif event.key in (pygame.K_DOWN, pygame.K_s) and game.direction != (0, -CELL_SIZE):
                    game.direction = (0, CELL_SIZE)
                elif event.key in (pygame.K_LEFT, pygame.K_a) and game.direction != (CELL_SIZE, 0):
                    game.direction = (-CELL_SIZE, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d) and game.direction != (-CELL_SIZE, 0):
                    game.direction = (CELL_SIZE, 0)
                elif event.key == pygame.K_r and game.game_over:
                    game.reset_game()

        game.step()
        game.render()

    pygame.quit()

if __name__ == "__main__":
    main()