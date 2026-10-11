"""Graphical version of Karel Goes to Manila.

Run with:
    python src/pygame_game.py

Install the only graphical dependency with:
    python -m pip install pygame-ce
"""

from __future__ import annotations

import random
import time
from dataclasses import dataclass
from pathlib import Path

import pygame


WIDTH, HEIGHT = 960, 720
GRID_ORIGIN = (40, 120)
CELL_SIZE = 52
FPS = 60
SCORES_PATH = Path(__file__).resolve().parent.parent / "highscore.txt"

COLORS = {
    "background": (20, 24, 34),
    "panel": (34, 40, 54),
    "street": (232, 220, 188),
    "wall": (75, 81, 94),
    "package": (245, 166, 35),
    "robot": (55, 164, 232),
    "text": (245, 245, 245),
    "muted": (174, 183, 198),
    "success": (90, 210, 130),
    "danger": (238, 95, 95),
}


@dataclass
class Player:
    name: str
    x: int = 1
    y: int = 1
    level: int = 1
    packages: int = 0
    score: int = 0
    battery: int = 0
    max_battery: int = 0
    facing: str = "East"


def generate_level(level: int) -> tuple[list[list[int]], int, int]:
    size = min(8 + level // 2, 15)
    grid = [[0 for _ in range(size)] for _ in range(size)]
    package_count = min(2 + level // 3, 8)
    barrier_count = min(5 + level * 3, int(size * size * 0.4))

    placed = 0
    while placed < package_count:
        x, y = random.randrange(size), random.randrange(size)
        if (x, y) != (1, 1) and grid[y][x] == 0:
            grid[y][x] = 2
            placed += 1

    placed = 0
    while placed < barrier_count:
        x, y = random.randrange(size), random.randrange(size)
        if (x, y) != (1, 1) and grid[y][x] == 0:
            grid[y][x] = 1
            placed += 1

    battery = 30 + size * 2 + package_count * 5
    return grid, package_count, battery


def draw_text(
    surface: pygame.Surface,
    font: pygame.font.Font,
    text: str,
    position: tuple[int, int],
    color: tuple[int, int, int] = COLORS["text"],
) -> None:
    surface.blit(font.render(text, True, color), position)


def draw_robot(
    surface: pygame.Surface, x: int, y: int, facing: str, font: pygame.font.Font
) -> None:
    left = GRID_ORIGIN[0] + x * CELL_SIZE
    top = GRID_ORIGIN[1] + y * CELL_SIZE
    center = (left + CELL_SIZE // 2, top + CELL_SIZE // 2)
    pygame.draw.circle(surface, COLORS["robot"], center, CELL_SIZE // 3)
    direction = {
        "North": (0, -14),
        "South": (0, 14),
        "East": (14, 0),
        "West": (-14, 0),
    }.get(facing, (14, 0))
    nose = (center[0] + direction[0], center[1] + direction[1])
    pygame.draw.circle(surface, COLORS["text"], nose, 5)
    pygame.draw.circle(surface, COLORS["background"], nose, 2)
    draw_text(surface, font, "K", (left + 17, top + 13), COLORS["text"])


def draw_grid(
    surface: pygame.Surface,
    grid: list[list[int]],
    player: Player,
    title_font: pygame.font.Font,
) -> None:
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            rect = pygame.Rect(
                GRID_ORIGIN[0] + x * CELL_SIZE,
                GRID_ORIGIN[1] + y * CELL_SIZE,
                CELL_SIZE - 2,
                CELL_SIZE - 2,
            )
            color = COLORS["wall"] if cell == 1 else COLORS["street"]
            pygame.draw.rect(surface, color, rect, border_radius=5)
            if cell == 2:
                pygame.draw.circle(surface, COLORS["package"], rect.center, 13)
                draw_text(surface, title_font, "P", (rect.x + 16, rect.y + 8), COLORS["text"])

    draw_robot(surface, player.x, player.y, player.facing, title_font)


def load_scores() -> list[tuple[str, int, int, float]]:
    scores: list[tuple[str, int, int, float]] = []
    if not SCORES_PATH.exists():
        return scores
    for line in SCORES_PATH.read_text(encoding="utf-8").splitlines():
        fields = line.split(",")
        if len(fields) != 4:
            continue
        try:
            scores.append((fields[0], int(fields[1]), int(fields[2]), float(fields[3])))
        except ValueError:
            continue
    return sorted(scores, key=lambda item: item[1], reverse=True)[:5]


def save_score(player: Player, elapsed: float) -> None:
    scores = load_scores()
    scores.append((player.name, player.score, player.level, round(elapsed, 2)))
    scores.sort(key=lambda item: item[1], reverse=True)
    SCORES_PATH.write_text(
        "".join(f"{name},{score},{level},{duration}\n" for name, score, level, duration in scores[:5]),
        encoding="utf-8",
    )


def move_player(player: Player, grid: list[list[int]], dx: int, dy: int) -> None:
    player.facing = {(0, -1): "North", (0, 1): "South", (-1, 0): "West", (1, 0): "East"}.get(
        (dx, dy), player.facing
    )
    target_x, target_y = player.x + dx, player.y + dy
    if (
        0 <= target_y < len(grid)
        and 0 <= target_x < len(grid[0])
        and grid[target_y][target_x] != 1
        and player.battery > 0
    ):
        player.x, player.y = target_x, target_y
        player.battery -= 1


def main() -> None:
    pygame.init()
    pygame.display.set_caption("Karel Goes to Manila")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    title_font = pygame.font.Font(None, 30)
    body_font = pygame.font.Font(None, 24)
    small_font = pygame.font.Font(None, 20)

    name = "Player"
    player = Player(name)
    grid, target_packages, player.max_battery = generate_level(player.level)
    player.battery = player.max_battery
    level_started = time.monotonic()
    game_over = False
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_r and game_over:
                    player = Player(name)
                    grid, target_packages, player.max_battery = generate_level(player.level)
                    player.battery = player.max_battery
                    level_started = time.monotonic()
                    game_over = False
                elif not game_over:
                    moves = {
                        pygame.K_w: (0, -1),
                        pygame.K_s: (0, 1),
                        pygame.K_a: (-1, 0),
                        pygame.K_d: (1, 0),
                    }
                    if event.key in moves:
                        move_player(player, grid, *moves[event.key])
                    elif event.key in (pygame.K_SPACE, pygame.K_p):
                        if grid[player.y][player.x] == 2:
                            grid[player.y][player.x] = 0
                            player.packages += 1

        elapsed = time.monotonic() - level_started
        if not game_over and player.packages == target_packages:
            player.score += player.battery * 10 + max(0, int((30 - elapsed) * 10))
            player.level += 1
            player.x, player.y, player.packages = 1, 1, 0
            grid, target_packages, player.max_battery = generate_level(player.level)
            player.battery = player.max_battery
            level_started = time.monotonic()
        elif not game_over and player.battery <= 0:
            save_score(player, elapsed)
            game_over = True

        screen.fill(COLORS["background"])
        pygame.draw.rect(screen, COLORS["panel"], (20, 20, WIDTH - 40, 75), border_radius=10)
        draw_text(screen, title_font, "KAREL GOES TO MANILA", (40, 35))
        draw_text(
            screen,
            body_font,
            f"Level {player.level}   Score {player.score}   "
            f"Packages {player.packages}/{target_packages}   Battery {player.battery}/{player.max_battery}",
            (40, 66),
        )
        draw_grid(screen, grid, player, title_font)
        side_x = GRID_ORIGIN[0] + len(grid[0]) * CELL_SIZE + 28
        draw_text(screen, title_font, "CONTROLS", (side_x, 130))
        draw_text(screen, small_font, "W A S D  Move", (side_x, 170), COLORS["muted"])
        draw_text(screen, small_font, "SPACE / P  Pick up", (side_x, 198), COLORS["muted"])
        draw_text(screen, small_font, "Q  Quit", (side_x, 226), COLORS["muted"])
        if game_over:
            draw_text(screen, title_font, "GAME OVER", (side_x, 285), COLORS["danger"])
            draw_text(screen, body_font, f"Final score: {player.score}", (side_x, 320))
            draw_text(screen, small_font, "Press R to restart", (side_x, 355), COLORS["muted"])
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
