from colors import Colors
from position import Position
import pygame

class Block:
    def __init__(self, id):
        self.id = id
        self.rotation_state = 0
        self.row_offset = 0
        self.col_offset = 0
        self.cells = {}
        self.cell_size = 30
        self.colors = Colors.get_cell_colors()

    def move(self, rows, cols):
        self.row_offset += rows
        self.col_offset += cols

    def rotate(self):
        self.rotation_state = (self.rotation_state + 1) % 4

    def undo_rotate(self):
        self.rotation_state = (self.rotation_state - 1) % 4

    def get_cell_positions(self):
        tiles = self.cells[self.rotation_state]
        moved_tiles = []
        for position in tiles:
            position = Position(position.row + self.row_offset, position.col + self.col_offset)
            moved_tiles.append(position)
        return moved_tiles


    def draw(self, screen, x_offset, y_offset):
        tiles = self.get_cell_positions()
        for tile in tiles:
            tile_rect = pygame.Rect(tile.col * self.cell_size + x_offset, tile.row * self.cell_size + y_offset,
                                    self.cell_size - 1, self.cell_size - 1)
            pygame.draw.rect(screen, self.colors[self.id], tile_rect)