import pygame
import sys
import random

GRID_SIZE = 12
TILE_W = 54
TILE_H = 28
ORIGIN_X = 400
ORIGIN_Y = 120
SCREEN_W = 800
SCREEN_H = 650

# Directions: 0=East (+X), 1=North (+Y), 2=West (-X), 3=South (-Y)
DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

class KarelSnakeGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Karel Snake: Manila Edition")
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 16, bold=True)
        self.big_font = pygame.font.SysFont("Arial", 32, bold=True)

        self.reset()

    def reset(self):
        # Snake body as a list of (x, y) coordinates. Head is index 0.
        self.body = [(2, 2), (1, 2), (0, 2)]
        self.facing = 0  # East
        self.score = 0
        self.game_over = False
        self.spawn_beeper()

    def spawn_beeper(self):
        while True:
            pos = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
            if pos not in self.body:
                self.beeper = pos
                break

    def grid_to_iso(self, gx, gy):
        iso_x = ORIGIN_X + (gx - gy) * (TILE_W // 2)
        iso_y = ORIGIN_Y + (gx + gy) * (TILE_H // 2)
        return iso_x, iso_y

    def step(self, turn_command=None):
        if self.game_over:
            return

        if turn_command == "LEFT":
            self.facing = (self.facing + 1) % 4
        elif turn_command == "RIGHT":
            self.facing = (self.facing - 1) % 4

        dx, dy = DIRS[self.facing]
        head_x, head_y = self.body[0]
        new_head = (head_x + dx, head_y + dy)

        # Wall Collision
        if not (0 <= new_head[0] < GRID_SIZE and 0 <= new_head[1] < GRID_SIZE):
            self.game_over = True
            return

        # Self Collision
        if new_head in self.body[:-1]:
            self.game_over = True
            return

        # Move head
        self.body.insert(0, new_head)

        # Check if beeper collected
        if new_head == self.beeper:
            self.score += 1
            self.spawn_beeper()
        else:
            self.body.pop()  # Remove tail if no food eaten

    def render(self):
        self.screen.fill((28, 32, 40))

        # 1. Draw Grid Tiles
        for gy in range(GRID_SIZE - 1, -1, -1):
            for gx in range(GRID_SIZE):
                cx, cy = self.grid_to_iso(gx, gy)
                pts = [
                    (cx, cy - TILE_H // 2),
                    (cx + TILE_W // 2, cy),
                    (cx, cy + TILE_H // 2),
                    (cx - TILE_W // 2, cy)
                ]
                pygame.draw.polygon(self.screen, (55, 60, 72), pts)
                pygame.draw.polygon(self.screen, (40, 44, 54), pts, 1)

        # 2. Draw Beeper (Gold Coin / Passenger token)
        bx, by = self.grid_to_iso(self.beeper[0], self.beeper[1])
        pygame.draw.circle(self.screen, (241, 196, 15), (bx, by), 9)
        pygame.draw.circle(self.screen, (243, 156, 18), (bx, by), 9, 2)

        # 3. Draw Snake Body (Tail to Head)
        for i, (seg_x, seg_y) in reversed(list(enumerate(self.body))):
            sx, sy = self.grid_to_iso(seg_x, seg_y)
            is_head = (i == 0)
            h = 22 if is_head else 14
            color = (231, 76, 60) if is_head else (52, 152, 219)

            # Drop shadow
            pygame.draw.ellipse(self.screen, (15, 18, 24), (sx - 14, sy - 4, 28, 12))

            # Isometric cube
            top = [(sx, sy - h - 5), (sx + 14, sy - h), (sx, sy - h + 5), (sx - 14, sy - h)]
            left = [(sx - 14, sy - h), (sx, sy - h + 5), (sx, sy + 5), (sx - 14, sy)]
            right = [(sx + 14, sy - h), (sx, sy - h + 5), (sx, sy + 5), (sx + 14, sy)]

            pygame.draw.polygon(self.screen, (int(color[0] * 0.75), int(color[1] * 0.75), int(color[2] * 0.75)), left)
            pygame.draw.polygon(self.screen, (int(color[0] * 0.9), int(color[1] * 0.9), int(color[2] * 0.9)), right)
            pygame.draw.polygon(self.screen, color, top)

        # Status Overlay
        score_text = self.font.render(f"Beepers Collected: {self.score} | Length: {len(self.body)}", True, (240, 240, 240))
        self.screen.blit(score_text, (20, 20))

        if self.game_over:
            msg = self.big_font.render("CRASH! Press R to Restart", True, (231, 76, 60))
            self.screen.blit(msg, (SCREEN_W // 2 - msg.get_width() // 2, SCREEN_H // 2))

        pygame.display.flip()