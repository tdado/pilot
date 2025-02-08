import pygame
from constants import *
from utils import *
from ui_system import UISystem
from game import Game
from wfc import initialize_wave_function
import numpy as np


def main():
    pygame.init()
    screen = pygame.display.set_mode((TILE_SIZE * GRID_COLS * ZOOM_FACTOR,
                                       TILE_SIZE * GRID_ROWS * ZOOM_FACTOR))
    sprite_sheet = pygame.image.load("Assets.png").convert_alpha()
    frames = preload_frames(sprite_sheet)
    ui = UISystem(screen, frames)
    adjacency_rules = load_adjacency_rules("dictionary.json")
    
    # PRACTICE TRIAL
    ui.show_intro_screen_1()
    ui.show_intro_screen_2()
    ui.show_intro_screen_3()
    game_1 = Game(
        wave_function=initialize_wave_function(OUTPUT_SHAPE, NUM_TILES),
        adjacency_rules=update_dictionary_with_weights(adjacency_rules, compute_weight_distribution(0.15)),
        tile_folder=f"env/env_8",
        tile_names=list(adjacency_rules.keys()),
        world_id=1,
        frames=frames
    )
    game_2 = Game(
        wave_function=initialize_wave_function(OUTPUT_SHAPE, NUM_TILES),
        adjacency_rules=update_dictionary_with_weights(adjacency_rules, compute_weight_distribution(0.1)),
        tile_folder=f"env/env_6",
        tile_names=list(adjacency_rules.keys()),
        world_id=2,
        frames=frames
    )
    game_1 = play(game_1, frames, ui)
    ui.show_transition_to_world_2_screen(game_1)
    game_2 = play(game_2, frames, ui)
    decision, conf = ui.show_decision_screen(game_2)
    # ui.show_intro_screen_4(game_1, game_2, decision, conf)
    current_game = ui.show_switch_instructions_screen(game_1, game_2, decision, conf)
    current_game = play(game_2, frames, ui, phase=2, switch=game_1)
    _, _ = ui.show_decision_screen(current_game)
    ui.show_practice_end_screen()

    # EXPERIMENT
    with open("pilot_log.txt", "w") as log_file, open("log_sum.txt", "w") as log_sum:
        log_file.write("trial_num\tdecision_num\tworld_id\tplayer_pos\ttile\tlooking_time\tdirection\n")
        log_sum.write("trial_num\tprob_world_1\tprob_world_2\t"
                "steps_world_1\tsteps_world_2\t"
                "stones_world_1\tstones_world_2\t"
                "decision_1\tdecision_2\tconf_1\tconf_2\n")
        for trial_number, (world_1, world_2) in enumerate(TRIALS):
            ui.show_start_screen(trial_number, world_1, world_2, trial_number >= 10)
            prob_world_1, prob_world_2 = PROBABILITIES[trial_number]
            weights_1 = compute_weight_distribution(prob_world_1)
            weights_2 = compute_weight_distribution(prob_world_2)
            game_1 = Game(
                wave_function=initialize_wave_function(OUTPUT_SHAPE, NUM_TILES),
                adjacency_rules=update_dictionary_with_weights(adjacency_rules, weights_1),
                tile_folder=f"env/env_{world_1}",
                tile_names=list(adjacency_rules.keys()),
                world_id=1,
                frames=frames
            )
            game_2 = Game(
                wave_function=initialize_wave_function(OUTPUT_SHAPE, NUM_TILES),
                adjacency_rules=update_dictionary_with_weights(adjacency_rules, weights_2),
                tile_folder=f"env/env_{world_2}",
                tile_names=list(adjacency_rules.keys()),
                world_id=2,
                frames=frames
            )

            # PHASE 1: EXPLORE WORLD 1
            game_1 = play(game_1, frames, ui, phase=0, log_file=log_file, trial_number=trial_number)
            ui.show_transition_to_world_2_screen(game_1)

            # PHASE 2: EXPLORE WORLD 2
            game_2 = play(game_2, frames, ui, phase=1, log_file=log_file, trial_number=trial_number)

            # PHASE 3: DECISION 1
            decision_1, conf_1 = ui.show_decision_screen(game_2)
            log_sum.write(f"{trial_number}\t{prob_world_1:.2f}\t{prob_world_2:.2f}\t"
                f"{game_1.steps}\t{game_2.steps}\t")
            
            # PHASE 4: SAMPLING
            current_game = ui.show_switch_instructions_screen(game_1, game_2, decision_1, conf_1)
            current_game = play(current_game, frames, ui, switch=game_2 if current_game == game_1 else game_1, phase=2, log_file=log_file, trial_number=trial_number)

            # PHASE 5: DECISION 2
            decision_2, conf_2 = ui.show_decision_screen(current_game)
            log_sum.write(f"{trial_number}\t{prob_world_1:.2f}\t{prob_world_2:.2f}\t"
                          f"{game_1.steps}\t{game_2.steps}\t"
                          f"{np.sum(get_tile_ids(game_1.wave_function, game_1.tile_names) == 12)}\t"
                          f"{np.sum(get_tile_ids(game_2.wave_function, game_2.tile_names) == 12)}\t"
                          f"{decision_1}\t{decision_2}\t{conf_1}\t{conf_2}\n")
    pygame.quit()


if __name__ == "__main__":
    main()                     