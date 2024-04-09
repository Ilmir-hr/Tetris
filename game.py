from blocks import *
from grid import Grid
import random
import pygame


class Game:
    def __init__(self):
        self.grid = Grid()
        self.blocks = self.get_random_list_of_blocks()
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.game_over = False
        self.score = 0
        self.clear_sound = pygame.mixer.Sound('Sounds/clear.mp3')
        self.rotate_sound = pygame.mixer.Sound('Sounds/rotate.mp3')
        pygame.mixer.music.load('Sounds/music.mp3')
        pygame.mixer.music.play(-1)

    def update_score(self, line_cleared, move_down_points):
        if line_cleared == 1:
            self.score += 100
        if line_cleared == 2:
            self.score += 300
        if line_cleared == 3:
            self.score += 500
        self.score += move_down_points
    @staticmethod
    def get_random_list_of_blocks():
        blocks = [LBlock(), TBlock(), OBlock(), IBlock(), JBlock(), SBlock(), ZBlock()]
        random.shuffle(blocks)
        return blocks

    def get_random_block(self):
        if self.blocks:
            return self.blocks.pop()
        self.blocks = self.get_random_list_of_blocks()
        return self.blocks.pop()

    def move_left(self):
        self.current_block.move(0, -1)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(0, 1)

    def move_right(self):
        self.current_block.move(0, 1)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(0, -1)

    def move_down(self):
        self.current_block.move(1, 0)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(-1, 0)
            self.lock_block()

    def lock_block(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            self.grid.grid[tile.row][tile.col] = self.current_block.id
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        rows_cleared = self.grid.clear_full_rows()
        if rows_cleared:
            self.clear_sound.play()
            self.update_score(rows_cleared, 0)
        if not self.block_fits():
            self.game_over = True

    def rotate(self):
        self.current_block.rotate()
        if not self.block_inside() or not self.block_fits():
            self.current_block.undo_rotate()
        else:
            self.rotate_sound.play()

    def block_inside(self):
        tiles = self.current_block.get_cell_positions()
        return all(self.grid.is_inside(tile.row, tile.col) for tile in tiles)

    def block_fits(self):
        tiles = self.current_block.get_cell_positions()
        return all(self.grid.is_empty(tile.row, tile.col) for tile in tiles)

    def reset(self):
        self.grid.reset()
        self.blocks = self.get_random_list_of_blocks()
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0

    def draw(self, screen):
        self.grid.draw(screen)
        self.current_block.draw(screen, 11, 11)
        if self.next_block.id == 3:
            self.next_block.draw(screen, 255, 290)
        elif self.next_block.id == 4:
            self.next_block.draw(screen, 255, 280)
        else:
            self.next_block.draw(screen, 270, 270)
