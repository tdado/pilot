import numpy as np
import pygame
import random
import scipy.ndimage


def apply_gaussian_blur(surface, sigma=1):
    arr = pygame.surfarray.pixels3d(surface)
    blurred_arr = np.zeros_like(arr)
    for i in range(3):
        blurred_arr[:, :, i] = scipy.ndimage.gaussian_filter(arr[:, :, i], sigma=sigma)
    return pygame.surfarray.make_surface(blurred_arr)

def generate_static_noise(tile_size, seed=42):
    """Generates a fixed noise pattern (doesn't change every frame)."""
    np.random.seed(seed)  # Ensure consistency across frames
    noise = np.random.randint(0, 7, (tile_size[0], tile_size[1], 3), dtype=np.uint8)
    surface = pygame.Surface(tile_size)
    pygame.surfarray.blit_array(surface, noise)
    return surface

STATIC_NOISE = generate_static_noise((16, 16))

def initialize_wave_function(output_shape, num_tiles):
    height, width = output_shape
    wave_function = np.full((height, width, num_tiles), True)
    return wave_function

def observe(wave_function, tile_names, dictionary, pos):
    y, x = pos
    weights = np.array([dictionary[tile]["weight"] for tile in tile_names])
    current_possibilities = wave_function[y, x]  # Use (y, x) indexing
    adjusted_weights = current_possibilities * weights
    sum_adjusted_weights = np.sum(adjusted_weights)
    if sum_adjusted_weights == 0:  # Handle contradictions gracefully
        print(f"Contradiction at ({y}, {x}): Tile left unresolved.")
        return wave_function  # Leave the tile as-is
    probabilities = adjusted_weights / sum_adjusted_weights
    chosen_tile_index = np.random.choice(len(tile_names), p=probabilities)
    wave_function[y, x] = False
    wave_function[y, x, chosen_tile_index] = True
    return wave_function

def propagate(wave_function, dictionary, pos, tile_names):
    fh, fw = wave_function.shape[:2]
    stack = [pos]
    while stack:
        y, x = stack.pop()
        for dy, dx, direction in [(-1, 0, "top"), (1, 0, "bottom"), (0, -1, "left"), (0, 1, "right")]:
            ny, nx = y + dy, x + dx
            if not (0 <= ny < fh and 0 <= nx < fw):
                continue
            neighbor_wave = wave_function[ny, nx]
            current_possibilities = set(tile_names[i] for i in range(len(tile_names)) if neighbor_wave[i])
            valid_neighbors = set() # Compute the union of all valid neighbors for all possible tiles
            for i in range(len(tile_names)):
                if wave_function[y, x, i]:  # Only consider valid tiles at (y, x)
                    valid_neighbors.update(str(neighbor[0]) for neighbor in dictionary[tile_names[i]][direction])
            new_possibilities = current_possibilities & valid_neighbors
            if not new_possibilities:
                print("Contradiction.")
                continue
            for i, tile_name in enumerate(tile_names): # Update the wave function with new possibilities
                if tile_name not in new_possibilities:
                    wave_function[ny, nx, i] = False
            if current_possibilities != new_possibilities: # If possibilities changed, propagate further
                stack.append((ny, nx))
    return wave_function

def visualize_wave_function(wave_function, player_pos, grid_shape, tile_images, tile_names, ZOOM):
    grid_rows, grid_cols = grid_shape
    height, width, _ = wave_function.shape
    tile_size = tile_images[tile_names[0]].get_size()  # Assume all tiles are the same size
    scaled_tile_size = (tile_size[0] * ZOOM, tile_size[1] * ZOOM)
    output_surface = pygame.Surface((grid_cols * scaled_tile_size[0], grid_rows * scaled_tile_size[1]), pygame.SRCALPHA)
    center_y, center_x = player_pos # center viewport around player
    half_rows = grid_rows // 2
    half_cols = grid_cols // 2
    min_x = max(0, center_x - half_cols)  # viewport bounds
    max_x = min(width, center_x + half_cols + 1)
    min_y = max(0, center_y - half_rows)
    max_y = min(height, center_y + half_rows + 1)
    if center_x - half_cols < 0:  # adjust for edges
        min_x = 0
        max_x = grid_cols
    elif center_x + half_cols >= width:
        max_x = width
        min_x = width - grid_cols
    if center_y - half_rows < 0:
        min_y = 0
        max_y = grid_rows
    elif center_y + half_rows >= height:
        max_y = height
        min_y = height - grid_rows
    for y in range(min_y, max_y):
        for x in range(min_x, max_x):
            possibilities = wave_function[y, x]
            if np.sum(possibilities) == 0:
                probabilities = np.zeros_like(possibilities)
            else:
                probabilities = possibilities / np.sum(possibilities)
            blended_tile = pygame.Surface(tile_size, pygame.SRCALPHA)
            blended_tile.fill((0, 0, 0, 0))  # Fully transparent surface
            is_superposition = np.max(probabilities) < 0.95
            for tile_idx, prob in enumerate(probabilities):
                if prob > 0:
                    tile_image = tile_images[tile_names[tile_idx]].copy()
                    alpha = int(prob * 255)
                    tile_image.set_alpha(min(255, alpha))
                    blended_tile.blit(tile_image, (0, 0))
            if is_superposition:
                blended_tile.fill((150, 150, 150), special_flags=pygame.BLEND_MULT)
                blended_tile.blit(STATIC_NOISE, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
                blended_tile = apply_gaussian_blur(blended_tile, sigma=3)  # Gentle blur

            scaled_tile = pygame.transform.scale(blended_tile, scaled_tile_size)
            screen_x = (x - min_x) * scaled_tile_size[0]
            screen_y = (y - min_y) * scaled_tile_size[1]
            output_surface.blit(scaled_tile, (screen_x, screen_y))
    return output_surface