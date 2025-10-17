import pygame

neighbor_dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]


class Tile:
    def __init__(
        self,
        x: int,
        y: int,
        name: str,
        color: tuple,
        strength: float,
    ):
        self.x = x
        self.y = y
        self.name = name
        self.color = color
        self.strength = strength
        self.neighbors = []

        self.pending_color = []

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            self.color,
            (
                self.x,
                self.y,
                1,
                1,
            ),
        )

    def change_color(self, color):
        self.color = color

    def add_neighbors(self, tiles):
        for n_dir in neighbor_dirs:
            try:
                neighbor = tiles[self.y + n_dir[1]][self.x + n_dir[0]]
                self.neighbors.append(neighbor)
            except IndexError:
                pass

    def leak(self):
        self.pending_color.append((self.color, self.strength * 1.5))
        for n in self.neighbors:
            n.pending_color.append((self.color, self.strength))

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"
