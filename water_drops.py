import pygame
import sys
import random
import numpy as np

from tile import Tile

# Initialize Pygame
pygame.init()

info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h
# Screen dimensions
# SCREEN_WIDTH = 1500
# SCREEN_HEIGHT = 800
SCALE = 25

DISPLAY_WIDTH = SCREEN_WIDTH // SCALE
DISPLAY_HEIGHT = SCREEN_HEIGHT // SCALE

INPUT_INTERVAL = 100  # input in ms

COLOR_CHANGE_CHANCE = 0.8

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
DARK_GREY = (100, 100, 100)
GREEN = (0, 255, 0)
GREY = (180, 180, 180)
PINK = (255, 190, 190)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

all_colors = [PINK, GREY, WHITE, DARK_GREY, GREEN, RED, BLUE]

ROYAL_BLUE = (65, 105, 225)
SKY_BLUE = (135, 206, 235)
NAVY_BLUE = (0, 0, 128)
POWDER_BLUE = (176, 224, 230)
MEDIUM_BLUE = (0, 0, 205)
DEEP_SKY_BLUE = (0, 191, 255)
LIGHT_SKY_BLUE = (135, 206, 250)
STEEL_BLUE = (70, 130, 180)
DODGER_BLUE = (30, 144, 255)
CADET_BLUE = (95, 158, 160)

colors = [
    ROYAL_BLUE,
    SKY_BLUE,
    NAVY_BLUE,
    POWDER_BLUE,
    MEDIUM_BLUE,
    DEEP_SKY_BLUE,
    LIGHT_SKY_BLUE,
    STEEL_BLUE,
    DODGER_BLUE,
    CADET_BLUE,
]

# Tiles
tiles = []
for y in range(int(SCREEN_HEIGHT / SCALE)):
    tile_row = []
    for x in range(int(SCREEN_WIDTH / SCALE)):
        color = random.choice(colors)
        tile_row.append(Tile(x, y, "tile", color, np.random.uniform(0.6, 0.6)))
    tiles.append(tile_row)

for row in tiles:
    for t in row:
        t.add_neighbors(tiles)

row_length = len(tiles[0])
col_length = len(tiles)


def main():
    x = 0
    y = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    # screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    display_surface = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    clock = pygame.time.Clock()

    # Main game loop
    while True:
        # Control the frame rate
        time_delta = clock.tick(1000 // INPUT_INTERVAL)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                x = x // SCALE
                y = y // SCALE
                click_color = random.choice(all_colors)
                tiles[y][x].change_color(click_color)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        random_x = np.random.randint(0, row_length)
        random_y = np.random.randint(0, col_length)

        if random.random() < COLOR_CHANGE_CHANCE:
            color = random.choice(colors)
            tiles[random_y][random_x].change_color(color)

        for row in tiles:
            for tile_ in row:
                tile_.leak()

        for row in tiles:
            for tile_ in row:
                if len(tile_.pending_color) == 0:
                    continue
                strength_sum = np.sum([strength for _, strength in tile_.pending_color])
                pending_color = np.sum(
                    [
                        np.array(color) * strength
                        for color, strength in tile_.pending_color
                    ],
                    axis=0,
                )
                new_color = np.round(pending_color / (strength_sum)).astype(int)
                # decide new color
                tile_.change_color(new_color)
                # reset pending color
                tile_.pending_color = []

        display_surface.fill(BLACK)
        for row in tiles:
            for tile_ in row:
                tile_.draw(display_surface)
        screen.blit(
            pygame.transform.scale(display_surface, (SCREEN_WIDTH, SCREEN_HEIGHT)),
            (0, 0),
        )
        pygame.display.flip()


if __name__ == "__main__":
    main()
