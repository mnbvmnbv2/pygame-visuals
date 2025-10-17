import pygame
import sys
import random
import numpy as np

from tile import Tile

# Screen dimensions
pygame.init()

info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h

FRAME_RATE_UPDATE = 20  # input in ms

# Colors
RED = (255, 0, 0)
PINK = (255, 190, 190)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
DARK_GREY = (100, 100, 100)
GREY = (180, 180, 180)
WHITE = (255, 255, 255)

colors = [PINK, GREY, WHITE, DARK_GREY]

NUM_STARS = 500
COLOR_CHANGE_CHANCE = 0.1

# Tiles
tiles = []
for i in range(NUM_STARS):
    x = np.random.randint(0, SCREEN_WIDTH)
    y = np.random.randint(0, SCREEN_HEIGHT)
    color = random.choice(colors)
    tiles.append(Tile(x, y, "star", color, 1.0))


def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    clock = pygame.time.Clock()

    # Main game loop
    while True:
        time_delta = clock.tick(1000 // FRAME_RATE_UPDATE)  # Control the frame rate
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        for tile_ in tiles:
            # dont change 80% of the time
            if random.random() > COLOR_CHANGE_CHANCE:
                continue
            # change color
            color = random.choice(colors)
            tile_.change_color(color)

        screen.fill(BLACK)
        for tile_ in tiles:
            tile_.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    main()
