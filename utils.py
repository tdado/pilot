import json
from copy import deepcopy
from constants import SPRITE_WIDTH, SPRITE_HEIGHT, ZOOM_FACTOR, FRAMES_CONFIG, COLUMN_PADDING, ROW_PADDING, STEPS_LIMIT
import numpy as np
import time
import random
import pygame


def generate_probabilities(num_trials=40, P_baseline=0.15):
    probability_levels = [
        (P_baseline, P_baseline),
        (P_baseline, 0.2),
        (P_baseline, 0.25),
        (P_baseline, 0.1),
        (P_baseline, 0.05)
    ]
    probabilities = probability_levels * (num_trials // len(probability_levels))  # 5 pairs × 4 times = 20 trials
    random.shuffle(probabilities)
    randomized_probabilities = [(p if random.choice([True, False]) else (p[1], p[0])) for p in probabilities]
    return randomized_probabilities


def compute_weight_distribution(prob_stone):
    weights = {
        1: 1 - prob_stone,
        12: prob_stone - (prob_stone / 3), # 0.1
        13: prob_stone / 3 # 0.05
    }
    return weights

def update_dictionary_with_weights(dictionary, weights):
    updated_dict = deepcopy(dictionary)
    for tile_id, tile_data in updated_dict.items():
        tile_data["weight"] = weights[int(tile_id)]
    return updated_dict

def load_adjacency_rules(filepath):
    with open(filepath, "r") as f:
        return json.load(f)
    
def preload_frames(sprite_sheet):
    sprite_scale = (SPRITE_WIDTH * ZOOM_FACTOR, SPRITE_HEIGHT * ZOOM_FACTOR)
    frames = {}
    for direction, indices in FRAMES_CONFIG.items():
        frames[direction] = [
            pygame.transform.scale(
                sprite_sheet.subsurface(pygame.Rect(
                    COLUMN_PADDING + i * SPRITE_WIDTH,
                    ROW_PADDING,
                    SPRITE_WIDTH,
                    SPRITE_HEIGHT
                )),
                sprite_scale
            ) for i in indices
        ]
    return frames

def get_tile_ids(wave_function, tile_names):
    height, width, _ = wave_function.shape
    tile_id_grid = np.full((height, width), -1, dtype=int)
    for y in range(height):
        for x in range(width):
            possibilities = wave_function[y, x]
            if possibilities.sum() == 1:
                tile_index = np.argmax(possibilities)
                tile_id_grid[y, x] = tile_names[tile_index]
    return tile_id_grid

def play(game, frames, ui, switch=None, phase=0, log_file=None, trial_number=0):
    total_steps = 0
    current_game = game
    start_time = time.time()
    while total_steps < STEPS_LIMIT:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                direction = None
                if event.key == pygame.K_UP:
                    direction = "up"
                elif event.key == pygame.K_DOWN:
                    direction = "down"
                elif event.key == pygame.K_LEFT:
                    direction = "left"
                elif event.key == pygame.K_RIGHT:
                    direction = "right" 
                elif event.key == pygame.K_1 and current_game.world_id != 1:
                    current_game, switch = switch, current_game
                    if log_file:
                        log_file.write(
                            f"{trial_number}\t{phase}\t{current_game.world_id}\t{total_steps}\t"
                            f"{current_game.player_pos}\t{current_game.tile_id}\t"
                            f"{time.time() - start_time:.3f}\tSWITCH_TO_1\n"
                        )
                    start_time = time.time()
                    continue
                elif event.key == pygame.K_2 and current_game.world_id != 2:
                    current_game, switch = switch, current_game
                    if log_file:
                        log_file.write(
                            f"{trial_number}\t{phase}\t{current_game.world_id}\t{total_steps}\t"
                            f"{current_game.player_pos}\t{current_game.tile_id}\t"
                            f"{time.time() - start_time:.3f}\tSWITCH_TO_2\n"
                        )
                    start_time = time.time()
                    continue
                if direction:
                    current_game.move_player(direction, frames)
                    if log_file:
                        log_file.write(
                            f"{trial_number}\t{phase}\t{current_game.world_id}\t{total_steps}\t"
                            f"{current_game.player_pos}\t{current_game.tile_id}\t"
                            f"{time.time() - start_time:.3f}\t{direction}\n"
                        )
                    start_time = time.time() # reset
                    total_steps += 1

        # Update the game screen
        ui.draw(
            current_game.get_visible_surface(),
            current_game.player_pos,
            current_game.direction,
            current_game.frame_index,
            current_game.world_id
        )
        if phase == 2:
            ui.render_switch_instructions()

        pygame.display.flip()
    return current_game