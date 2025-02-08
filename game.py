import pygame
import numpy as np
from wfc import *
import os
from constants import *


class Game:
    def __init__(self, wave_function, adjacency_rules, tile_folder, tile_names, world_id, frames):
        self.wave_function = wave_function
        self.adjacency_rules = adjacency_rules
        self.tile_folder = tile_folder
        self.tile_names = tile_names
        self.world_id = world_id
        self.steps = 0
        self.direction = "down"
        self.frame_index = 0
        self.player_pos = [OUTPUT_SHAPE[0] // 2, OUTPUT_SHAPE[1] // 2]
        self.tile_surfaces = self.load_tiles()
        self.wave_function = observe(self.wave_function, self.tile_names, self.adjacency_rules, self.player_pos)
        self.wave_function = propagate(self.wave_function, self.adjacency_rules, tuple(self.player_pos), self.tile_names)
        self.frames = frames
        self.tile_id = str(self.tile_names[np.argmax(self.wave_function[self.player_pos])])

    def load_tiles(self):
        return {
            str(i): pygame.image.load(os.path.join(self.tile_folder, f"{i}.png"))
            for i in [1, 12, 13]
        }

    def get_visible_surface(self):
        return visualize_wave_function(
            self.wave_function,
            self.player_pos,
            (GRID_ROWS, GRID_COLS),
            self.tile_surfaces,
            self.tile_names,
            ZOOM_FACTOR
        )
        
    def move_player(self, direction, frames):
        if direction != self.direction:
            self.frame_index = 0 
        self.direction = direction
        dx, dy = 0, 0
        if direction == "up":
            dx = -1
        elif direction == "down":
            dx = 1
        elif direction == "left":
            dy = -1
        elif direction == "right":
            dy = 1
        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy
        if 0 <= new_x < OUTPUT_SHAPE[0] and 0 <= new_y < OUTPUT_SHAPE[1]:
            temp_wave_function = observe(self.wave_function, self.tile_names, self.adjacency_rules, [new_x, new_y])
            # tile_index = np.argmax(temp_wave_function[new_x, new_y])
            # tile_id = str(self.tile_names[tile_index])
            self.wave_function = propagate(temp_wave_function, self.adjacency_rules, (new_x, new_y), self.tile_names)
            # if tile_id not in UNWALKABLE_TILES:
            self.player_pos = [new_x, new_y]
            self.frame_index = (self.frame_index + 1) % len(frames[self.direction])
            self.steps += 1
