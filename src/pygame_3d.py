"""First-person 3D-style Karel game using a lightweight raycaster.

Run:
    python src/pygame_3d.py

This keeps the existing grid gameplay but renders walls and streets in
perspective without requiring a full 3D engine.
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass

import pygame

from pygame_game import generate_level, load_scores, save_score


WIDTH, HEIGHT = 1000, 700
FOV = math.pi / 3
RAY_COUNT = 240
MAX_DEPTH = 20
MOVE_SPEED = 2.4
TURN_SPEED = 2.4

SKY = (77, 135, 184)
GROUND = (55, 54, 52)
WALL_COLORS = ((112, 73, 54), (82, 94, 111), (127, 86, 54))
PACKAGE_COLOR = (248, 184, 42)
TEXT_COLOR = (245, 245, 245)


@dataclass
class Player:
    name: str = "Player"
    x: float = 1.5
    y: float = 1.5
    angle: float = 0.0
    battery: float = 0
    max_battery: int = 0
    packages: int = 0
    score: int = 0
    level: int = 1


def is_open(grid: list[list[int]], x: float, y: float) -> bool:
    cell_x, cell_y = int(x), int(y)
    return (
        0 <= cell_y < len(grid)
        and 0 <= cell_x < len(grid[0])
        and grid[cell_y][cell_x] != 1
    )


def move_player(player: Player, grid: list[list[int]], dx: float, dy: float) -> None:
    if player.battery <= 0:
        return
    if is_open(grid, player.x + dx, player.y):
        player.x += dx
    if is_open(grid, player.x, player.y + dy):
        player.y += dy
    player.battery -= max(abs(dx), abs(dy))


def cast_walls(
    screen: pygame.Surface, grid: list[list[int]], player: Player
) -> list[float]:
    pygame.draw.rect(screen, SKY, (0, 0, WIDTH, HEIGHT // 2))
    pygame.draw.rect(screen, GROUND, (0, HEIGHT // 2, WIDTH, HEIGHT // 2))
    depths: list[float] = []
    column_width = WIDTH / RAY_COUNT

    for ray in range(RAY_COUNT):
        ray_angle = player.angle - FOV / 2 + FOV * ray / RAY_COUNT
        sin_a, cos_a = math.sin(ray_angle), math.cos(ray_angle)
        depth = 0.05
        hit = False
        cell = 1
        while depth < MAX_DEPTH:
            test_x = player.x + cos_a * depth
            test_y = player.y + sin_a * depth
            if not is_open(grid, test_x, test_y):
                cell_x, cell_y = int(test_x), int(test_y)
                if 0 <= cell_y < len(grid) and 0 <= cell_x < len(grid[0]):
                    cell = grid[cell_y][cell_x]
                else:
                    cell = 1
                hit = True
                break
            depth += 0.025

        corrected_depth = depth * math.cos(ray_angle - player.angle)
        depths.append(corrected_depth)
        if not hit:
            continue
        wall_height = min(HEIGHT * 2, HEIGHT / max(corrected_depth, 0.01))
        shade = max(35, 255 - int(corrected_depth * 18))
        base = WALL_COLORS[cell % len(WALL_COLORS)]
        color = tuple(max(0, int(channel * shade / 255)) for channel in base)
        x = int(ray * column_width)
        pygame.draw.rect(
            screen,
            color,
            (x, int(HEIGHT / 2 - wall_height / 2), math.ceil(column_width) + 1, wall_height),
        )
    return depths


def draw_packages(
    screen: pygame.Surface,
    grid: list[list[int]],
    player: Player,
    depths: list[float],
) -> None:
    packages: list[tuple[float, float, float, int]] = []
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell != 2:
                continue
            dx, dy = x + 0.5 - player.x, y + 0.5 - player.y
            distance = math.hypot(dx, dy)
            angle = math.atan2(dy, dx) - player.angle
            angle = (angle + math.pi) % (2 * math.pi) - math.pi
            if abs(angle) < FOV / 2 and distance > 0.1:
                screen_x = int((angle / FOV + 0.5) * WIDTH)
                ray_index = min(RAY_COUNT - 1, max(0, int(screen_x / WIDTH * RAY_COUNT)))
                packages.append((distance, angle, screen_x, ray_index))

    for distance, _, screen_x, ray_index in sorted(packages, reverse=True):
        if distance >= depths[ray_index]:
            continue
        size = max(8, int(130 / distance))
        y = HEIGHT // 2 + int(45 / distance)
        pygame.draw.rect(
            screen, PACKAGE_COLOR, (screen_x - size // 2, y - size, size, size), border_radius=4
        )
        pygame.draw.rect(
            screen, (120, 75, 18), (screen_x - size // 2, y - size, size, size), 2
        )


def draw_hud(
    screen: pygame.Surface,
    font: pygame.font.Font,
    player: Player,
    target_packages: int,
    elapsed: float,
    game_over: bool,
) -> None:
    pygame.draw.rect(screen, (18, 20, 28), (0, 0, WIDTH, 66))
    text = (
        f"Level {player.level}   Score {player.score}   "
        f"Packages {player.packages}/{target_packages}   "
        f"Battery {player.battery}/{player.max_battery}   Time {elapsed:.1f}s"
    )
    screen.blit(font.render(text, True, TEXT_COLOR), (20, 18))
    controls = "W/S move  A/D turn  SPACE pick up  Q quit"
    screen.blit(font.render(controls, True, (195, 205, 215)), (20, HEIGHT - 38))
    if game_over:
        message = font.render("GAME OVER - press R to restart or Q to quit", True, (255, 105, 105))
        screen.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT // 2 - 100))


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Karel Goes to Manila - 3D")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 28)

    player = Player()
    grid, target_packages, player.max_battery = generate_level(player.level)
    player.battery = player.max_battery
    started = time.monotonic()
    game_over = False
    running = True

    while running:
        delta = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_SPACE and not game_over:
                    cell_x, cell_y = int(player.x), int(player.y)
                    if grid[cell_y][cell_x] == 2:
                        grid[cell_y][cell_x] = 0
                        player.packages += 1
                elif event.key == pygame.K_r and game_over:
                    player = Player()
                    grid, target_packages, player.max_battery = generate_level(player.level)
                    player.battery = player.max_battery
                    started = time.monotonic()
                    game_over = False

        if not game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                player.angle -= TURN_SPEED * delta
            if keys[pygame.K_d]:
                player.angle += TURN_SPEED * delta
            forward = (keys[pygame.K_w] - keys[pygame.K_s]) * MOVE_SPEED * delta
            if forward:
                move_player(
                    player,
                    grid,
                    math.cos(player.angle) * forward,
                    math.sin(player.angle) * forward,
                )

            elapsed = time.monotonic() - started
            if player.packages == target_packages:
                player.score += player.battery * 10 + max(0, int((30 - elapsed) * 10))
                player.level += 1
                player.x, player.y, player.angle, player.packages = 1.5, 1.5, 0.0, 0
                grid, target_packages, player.max_battery = generate_level(player.level)
                player.battery = player.max_battery
                started = time.monotonic()
            elif player.battery <= 0:
                save_score(player, elapsed)
                game_over = True
        else:
            elapsed = time.monotonic() - started

        depths = cast_walls(screen, grid, player)
        draw_packages(screen, grid, player, depths)
        draw_hud(screen, font, player, target_packages, elapsed, game_over)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
