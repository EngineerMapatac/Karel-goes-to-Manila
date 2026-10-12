import pygame
import sys
from karel_snake import KarelSnakeGame

def main():
    game = KarelSnakeGame()
    move_delay = 200  # Milliseconds per step
    last_move_time = pygame.time.get_ticks()

    pending_turn = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    pending_turn = "LEFT"
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    pending_turn = "RIGHT"
                elif event.key == pygame.K_r:
                    game.reset()

        # Step timer
        current_time = pygame.time.get_ticks()
        if current_time - last_move_time > move_delay:
            game.step(pending_turn)
            pending_turn = None
            last_move_time = current_time

        game.render()
        game.clock.tick(60)

if __name__ == "__main__":
    main()