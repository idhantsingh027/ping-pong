import pygame
import sys
from game.game_engine import GameEngine

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()

# Game instance
game = GameEngine(WIDTH, HEIGHT)

# Main loop
def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        game.handle_input()
        game.update()
        game.render(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
