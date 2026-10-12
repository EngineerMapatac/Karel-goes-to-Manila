import pygame
import sys
from karel_snake import KarelSnake2D

def main():
    game = KarelSnake2D()
    last_move_time = pygame.time.get_ticks()
    pending_turn = None

    while True:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            if event.type == pygame.KEYDOWN:
                # Menu Screen Navigation
                if game.state == "MENU":
                    if event.key in (pygame.K_1, pygame.K_KP1, pygame.K_RETURN):
                        game.reset_full_game()
                        game.state = "PLAYING"
                        last_move_time = current_time
                    elif event.key in (pygame.K_2, pygame.K_KP2, pygame.K_h):
                        game.state = "HIGH_SCORES"
                    elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                        pygame.quit()
                        sys.exit(0)

                # High Scores Screen Navigation
                elif game.state == "HIGH_SCORES":
                    if event.key in (pygame.K_m, pygame.K_ESCAPE, pygame.K_RETURN):
                        game.state = "MENU"

                # Gameplay Controls
                elif game.state == "PLAYING":
                    if event.key in (pygame.K_LEFT, pygame.K_a):
                        pending_turn = "LEFT"
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        pending_turn = "RIGHT"
                    elif event.key == pygame.K_ESCAPE:
                        game.state = "MENU"

                # Game Over Controls
                elif game.state == "GAME_OVER":
                    if event.key in (pygame.K_r, pygame.K_RETURN):
                        game.reset_full_game()
                        game.state = "PLAYING"
                        last_move_time = current_time
                    elif event.key in (pygame.K_m, pygame.K_ESCAPE):
                        game.state = "MENU"

        # Game step timer (speed increases each level)
        if game.state == "PLAYING":
            if current_time - last_move_time > game.move_delay:
                game.step(pending_turn)
                pending_turn = None
                last_move_time = current_time

        game.render()
        game.clock.tick(60)

if __name__ == "__main__":
    main()