import pygame

# Game Constants
TILE_SIZE = 16
GRID_ROWS = 6
GRID_COLS = 6
NUM_TILES = 3
STEPS_LIMIT = 50
N = 25
ZOOM_FACTOR = 8
NUM_TRIALS = 20
DECISIONS_PER_TRIAL = 2
SCREEN_WIDTH = TILE_SIZE * GRID_COLS * ZOOM_FACTOR
SCREEN_HEIGHT = TILE_SIZE * GRID_ROWS * ZOOM_FACTOR

# Sprite Configuration
SPRITE_WIDTH = 16
SPRITE_HEIGHT = 16
ROW_PADDING = 16
COLUMN_PADDING = 16
FRAMES_CONFIG = {
    "down": [0, 2],
    "left": [8, 9],
    "right": [6, 7],
    "up": [3, 5],
}

UNWALKABLE_TILES = {str(i) for i in range(6, 10)}
TRIALS = [(1, 5),
 (1, 8),
 (3, 7),
 (2, 6),
 (1, 8),
 (8, 10),
 (3, 9),
 (6, 7),
 (4, 7),
 (2, 6),
 (1, 5),
 (8, 9),
 (4, 9),
 (3, 5),
 (5, 6),
 (2, 3),
 (7, 10),
 (2, 4),
 (4, 10),
 (9, 10)]

OUTPUT_SHAPE = (N, N)

from utils import generate_probabilities  
PROBABILITIES = generate_probabilities()
