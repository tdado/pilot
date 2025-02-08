import pygame
from wfc import visualize_wave_function 
from constants import *


class UISystem:
    def __init__(self, screen, frames):
        self.screen = screen
        self.frames = frames
        self.font = pygame.font.Font("PokemonGb-RAeo.ttf", 16)

    def show_intro_screen_1(self):
        self.screen.fill((0, 0, 0))
        font = self.font
        lines = [
            ("Welcome, this is a practice round.", (255, 255, 255)),
            ("You are about to explore two planets.", (255, 255, 255)),
            ("", (0, 0, 0)),  # Empty line for spacing
            ("Press ENTER to continue...", (255, 255, 255)),
        ]
        line_height = font.size("Welcome, this is a practice round.")[1]
        total_height = len(lines) * line_height + (len(lines) - 1) * 10
        start_y = (self.screen.get_height() - total_height) // 2
        y = start_y
        for line in lines:
            text = font.render(line[0], True, line[1])
            self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, y))
            y += line_height + 10
        pygame.display.flip()
        self._wait_for_key(pygame.K_RETURN)

    def show_intro_screen_2(self):
        self.screen.fill((0, 0, 0))
        font = self.font
        lines = [
            ("Your one and only mission:", (255, 255, 255)),
            ("Find out which planet has more mushrooms", (255, 255, 255)),
            ("(they are randomly spread out)", (150, 150, 150)),
            ("", (0, 0, 0)),
            ("Mushrooms look like this:", (255, 255, 255))
        ]
        tile_1 = pygame.image.load("env/env_8/f.png").convert_alpha()
        tile_2 = pygame.image.load("env/env_6/f.png").convert_alpha()
        tile_1 = pygame.transform.scale(tile_1, (64, 64))
        tile_2 = pygame.transform.scale(tile_2, (64, 64))
        gap = 100
        total_width = tile_1.get_width() + tile_2.get_width() + gap
        text_heights = sum(font.size(line[0])[1] for line in lines) + len(lines) * 10
        tile_height = tile_1.get_height() + 40
        label_height = font.size("Planet 1")[1] + 20
        final_text_height = font.size("Press ENTER to continue...")[1] + 20
        total_height = text_heights + tile_height + label_height + final_text_height
        start_y = (self.screen.get_height() - total_height) // 2
        y = start_y
        for line in lines:
            text = font.render(line[0], True, line[1])
            self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, y))
            y += font.size(line[0])[1] + 10
        y += 20  # Space before tiles
        start_x = self.screen.get_width() // 2 - total_width // 2
        self.screen.blit(tile_1, (start_x, y))
        self.screen.blit(tile_2, (start_x + tile_1.get_width() + gap, y))
        y += tile_1.get_height() + 10
        label_font = self.font
        world_1_label = label_font.render("Planet 1", True, (255, 255, 255))
        world_2_label = label_font.render("Planet 2", True, (255, 255, 255))
        self.screen.blit(world_1_label, (start_x + tile_1.get_width() // 2 - world_1_label.get_width() // 2, y))
        self.screen.blit(world_2_label, (start_x + tile_1.get_width() + gap + tile_2.get_width() // 2 - world_2_label.get_width() // 2, y))
        y += 50
        final_text = font.render("Press ENTER to continue...", True, (255, 255, 255))
        self.screen.blit(final_text, (self.screen.get_width() // 2 - final_text.get_width() // 2, y))
        pygame.display.flip()
        self._wait_for_key(pygame.K_RETURN)

    def show_intro_screen_3(self):
        self.screen.fill((0, 0, 0))
        font = self.font
        lines = [
            ("First, take 50 steps on planet 1", (255, 255, 255)),
            ("", (0, 0, 0)),
            ("Use the ", (255, 255, 255)),
            ("[arrow keys]", (0, 255, 0)),
            (" to move around", (255, 255, 255)),
            ("", (0, 0, 0)),
        ]
        text_heights = sum(font.size(line[0])[1] for line in lines) + len(lines) * 10
        final_text_height = font.size("Press ENTER to begin")[1] + 20
        total_height = text_heights + final_text_height
        start_y = (self.screen.get_height() - total_height) // 2
        y = start_y
        for line in lines:
            text = font.render(line[0], True, line[1])
            self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, y))
            y += font.size(line[0])[1] + 10 
        final_text = font.render("Press ENTER to begin", True, (255, 255, 255))
        self.screen.blit(final_text, (self.screen.get_width() // 2 - final_text.get_width() // 2, y))
        pygame.display.flip()
        self._wait_for_key(pygame.K_RETURN)

    def show_intro_screen_4(self, game1, game2, decision, conf):
        self.screen.fill((0, 0, 0))
        font = self.font
        lines = [
            (f"You believe planet {int(decision)} has more mushrooms", (255, 255, 255)),
            ("", (0, 0, 0)),  # Spacing
            ("Now, practice switching between planets:", (255, 255, 255)),
            [("Press ", (255, 255, 255)), ("[1]", (0, 255, 0)), (" for Planet 1", (255, 255, 255))],  # Green [1]
            [("Press ", (255, 255, 255)), ("[2]", (0, 255, 0)), (" for Planet 2", (255, 255, 255))],  # Green [2]
            ("", (0, 0, 0)),  # Spacing
        ]
        text_heights = sum(font.size(line[0])[1] for line in lines if isinstance(line, tuple)) + len(lines) * 10
        total_height = text_heights
        start_y = (self.screen.get_height() - total_height) // 2
        y = start_y
        for line in lines:
            if isinstance(line, tuple):  # Regular text
                text = font.render(line[0], True, line[1])
                text_width, text_height = text.get_size()
                box_x = (self.screen.get_width() - text_width - 20) // 2  # Centering with padding
                pygame.draw.rect(self.screen, (0, 0, 0), (box_x, y - 5, text_width + 20, text_height + 10))  # Black box
                self.screen.blit(text, (self.screen.get_width() // 2 - text_width // 2, y))
                y += text_height + 10
            else:  # Text segments with different colors
                segments = line
                total_width = sum(font.render(segment[0], True, segment[1]).get_width() for segment in segments)
                text_height = font.size(segments[0][0])[1]
                box_x = (self.screen.get_width() - total_width - 20) // 2  # Centering with padding
                pygame.draw.rect(self.screen, (0, 0, 0), (box_x, y - 5, total_width + 20, text_height + 10))  # Black box
                x = self.screen.get_width() // 2 - total_width // 2
                for segment in segments:
                    segment_surface = font.render(segment[0], True, segment[1])
                    self.screen.blit(segment_surface, (x, y))
                    x += segment_surface.get_width()
                y += text_height + 10
        pygame.display.flip()
        waiting = True
        current_game = None
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        current_game = game1
                        waiting = False
                    elif event.key == pygame.K_2:
                        current_game = game2
                        waiting = False
        current_world_id = current_game.world_id  # Track current world
        switch_count = 0
        while switch_count < 6:
            self._render_practice_switch_screen(current_game, switch_count)
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1 and current_world_id != 1:
                            current_game = game1
                            current_world_id = 1
                            switch_count += 1
                            waiting = False
                        elif event.key == pygame.K_2 and current_world_id != 2:
                            current_game = game2
                            current_world_id = 2
                            switch_count += 1
                            waiting = False
        self._render_practice_switch_screen(current_game, switch_count)
        self._show_well_done_screen()
        _ = self.show_switch_instructions_screen(game1, game2, decision, conf)

    def _show_well_done_screen(self):
        self.screen.fill((0, 0, 0))
        font = self.font
        lines = [
            ("WELL DONE", (255, 255, 255)),
            ("Press ENTER to continue...", (255, 255, 255)),
        ]
        line_height = font.size("WELL DONE")[1]
        total_height = len(lines) * line_height + (len(lines) - 1) * 10
        start_y = (self.screen.get_height() - total_height) // 2
        y = start_y
        for line in lines:
            text = font.render(line[0], True, line[1])
            self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, y))
            y += line_height + 10
        pygame.display.flip()
        self._wait_for_key(pygame.K_RETURN)

    def _render_practice_switch_screen(self, game, switch_count):
        current_world_image = visualize_wave_function(
            game.wave_function,
            game.player_pos,
            (GRID_ROWS, GRID_COLS),
            game.tile_surfaces,
            game.tile_names,
            ZOOM_FACTOR
        )
        image_x = (SCREEN_WIDTH - current_world_image.get_width()) // 2
        image_y = (SCREEN_HEIGHT - current_world_image.get_height()) // 2
        self.screen.fill((0, 0, 0))
        self.screen.blit(current_world_image, (image_x, image_y))
        font = self.font
        label_font = pygame.font.Font(None, 36)
        label_text = f"Planet {game.world_id}"
        label_surface = label_font.render(label_text, True, (255, 255, 255))
        label_width = label_surface.get_width() + 20
        label_height = label_surface.get_height() + 10
        pygame.draw.rect(self.screen, (50, 50, 50), (10, 10, label_width, label_height))  # Dark background
        self.screen.blit(label_surface, (20, 15))
        instructions = [
            (f"Switch planets: {switch_count} / 6", (255, 255, 255)),  # Updated text
            None,  # Placeholder for styled instruction
        ]
        y = SCREEN_HEIGHT - 140  # Move up slightly
        text_box_width = 750  # Wider background box
        text_box_height = 100  # Taller background box
        text_box_x = (SCREEN_WIDTH - text_box_width) // 2
        text_box_y = y - 10
        text_bg = pygame.Surface((text_box_width, text_box_height), pygame.SRCALPHA)
        text_bg.fill((0, 0, 0, 180))  
        self.screen.blit(text_bg, (text_box_x, text_box_y))
        for idx, line in enumerate(instructions):
            if line:
                text = font.render(line[0], True, line[1])
                self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, y))
            else:
                segments = [
                    ("Press ", (255, 255, 255)),
                    ("'1'", (0, 255, 0)),
                    (" for Planet 1 or ", (255, 255, 255)),
                    ("'2'", (0, 255, 0)),
                    (" for Planet 2", (255, 255, 255)),
                ]
                x = SCREEN_WIDTH // 2 - sum(font.render(segment[0], True, segment[1]).get_width() for segment in segments) // 2
                for segment in segments:
                    segment_text = font.render(segment[0], True, segment[1])
                    self.screen.blit(segment_text, (x, y))
                    x += segment_text.get_width()
            y += 40
        pygame.display.flip()

    def show_practice_end_screen(self):
        self.screen.fill((0, 0, 0))
        font = self.font
        text = font.render("WELL DONE. The real experiment starts now", True, (255, 255, 255))
        self.screen.blit(
            text,
            (self.screen.get_width() // 2 - text.get_width() // 2,
            self.screen.get_height() // 2 - 20)  # Position slightly above the center
        )
        additional_text = font.render("Press ENTER to begin", True, (255, 255, 255))
        self.screen.blit(
            additional_text,
            (self.screen.get_width() // 2 - additional_text.get_width() // 2,
            self.screen.get_height() // 2 + 20)  # Position slightly below the main message
        )
        pygame.display.flip()
        self._wait_for_key(pygame.K_RETURN)

    def draw(self, visible_surface, player_pos, direction, frame_index, world_id):
        self.screen.fill((0, 0, 0))
        self.screen.blit(visible_surface, (0, 0))
        center_y, center_x = player_pos
        half_grid_rows = GRID_ROWS // 2
        half_grid_cols = GRID_COLS // 2
        if center_x - half_grid_cols < 0:
            screen_x = center_x * TILE_SIZE * ZOOM_FACTOR
        elif center_x + half_grid_cols >= OUTPUT_SHAPE[1]:
            screen_x = (center_x - (OUTPUT_SHAPE[1] - GRID_COLS)) * TILE_SIZE * ZOOM_FACTOR
        else:
            screen_x = (GRID_COLS // 2) * TILE_SIZE * ZOOM_FACTOR
        if center_y - half_grid_rows < 0:
            screen_y = center_y * TILE_SIZE * ZOOM_FACTOR
        elif center_y + half_grid_rows >= OUTPUT_SHAPE[0]:
            screen_y = (center_y - (OUTPUT_SHAPE[0] - GRID_ROWS)) * TILE_SIZE * ZOOM_FACTOR
        else:
            screen_y = (GRID_ROWS // 2) * TILE_SIZE * ZOOM_FACTOR
        screen_x += (TILE_SIZE * ZOOM_FACTOR) // 2 - (SPRITE_WIDTH * ZOOM_FACTOR) // 2
        screen_y += (TILE_SIZE * ZOOM_FACTOR) // 2 - (SPRITE_HEIGHT * ZOOM_FACTOR) // 2
        frame_count = len(self.frames[direction])
        current_frame = self.frames[direction][frame_index % frame_count]
        self.screen.blit(current_frame, (screen_x, screen_y))
        label_font = pygame.font.Font(None, 36)
        label_text = f"Planet {world_id}"
        label_surface = label_font.render(label_text, True, (255, 255, 255))
        label_width = label_surface.get_width() + 20
        label_height = label_surface.get_height() + 10
        pygame.draw.rect(
            self.screen,
            (0, 0, 0),  # Black background
            (10, 10, label_width, label_height)
        )
        self.screen.blit(label_surface, (20, 15))

    def show_start_screen(self, trial_number, env_1, env_2, ask_less=False):
        self.screen.fill((0, 0, 0))
        font = self.font
        question_base = "Which planet has"
        question_target = " less " if ask_less else " more "
        question_end = "mushrooms, you believe?"
        target_color_1 = (30, 144, 255) if not ask_less else (255, 127, 80)  # Blue for "more," red for "less"
        target_color_2 = (255, 255, 255)  # White for non-blinking state
        blinking_enabled = trial_number in [0, 10]  # First trial and 11th trial
        blinking = True
        last_blink_time = pygame.time.get_ticks()  # Initialize blinking timer
        tile_1 = pygame.image.load(f"env/env_{env_1}/f.png").convert_alpha()
        tile_2 = pygame.image.load(f"env/env_{env_2}/f.png").convert_alpha()
        tile_1 = pygame.transform.scale(tile_1, (64, 64))
        tile_2 = pygame.transform.scale(tile_2, (64, 64))
        gap = 100
        total_width = tile_1.get_width() + tile_2.get_width() + gap
        trial_text = font.render(f"Trial {trial_number + 1} / {NUM_TRIALS}", True, (255, 255, 255))
        start_text = font.render("Press ENTER to start", True, (255, 255, 255))
        text_height = trial_text.get_height() + 100  # Leave extra room for the question
        tile_height = tile_1.get_height() + 30
        start_text_height = start_text.get_height()
        total_height = text_height + tile_height + start_text_height + 80
        start_y = (self.screen.get_height() - total_height) // 2
        running = True
        while running:
            self.screen.fill((0, 0, 0))  # Clear the screen
            self.screen.blit(trial_text, (
                self.screen.get_width() // 2 - trial_text.get_width() // 2,
                start_y
            ))
            if blinking_enabled:
                current_time = pygame.time.get_ticks()
                if current_time - last_blink_time > 500:  # Blink every 500ms (0.5 seconds)
                    blinking = not blinking
                    last_blink_time = current_time  # Reset timer
            target_color = target_color_1 if (blinking and blinking_enabled) else target_color_2
            base_text = font.render(question_base, True, (255, 255, 255))
            target_text = font.render(question_target, True, target_color)
            end_text = font.render(question_end, True, (255, 255, 255))
            question_x = self.screen.get_width() // 2 - (
                base_text.get_width() + target_text.get_width() + end_text.get_width()
            ) // 2
            question_y = start_y + trial_text.get_height() + 40
            self.screen.blit(base_text, (question_x, question_y))
            question_x += base_text.get_width()
            self.screen.blit(target_text, (question_x, question_y))
            question_x += target_text.get_width()
            self.screen.blit(end_text, (question_x, question_y))
            labels_y = question_y + base_text.get_height() + 20
            label_font = self.font
            world_1_label = label_font.render("Planet 1", True, (255, 255, 255))
            world_2_label = label_font.render("Planet 2", True, (255, 255, 255))
            start_x = self.screen.get_width() // 2 - total_width // 2
            self.screen.blit(world_1_label, (start_x + tile_1.get_width() // 2 - world_1_label.get_width() // 2, labels_y))
            self.screen.blit(world_2_label, (start_x + tile_1.get_width() + gap + tile_2.get_width() // 2 - world_2_label.get_width() // 2, labels_y))
            tile_y = labels_y + world_1_label.get_height() + 20
            self.screen.blit(tile_1, (start_x, tile_y))
            self.screen.blit(tile_2, (start_x + tile_1.get_width() + gap, tile_y))
            self.screen.blit(start_text, (
                self.screen.get_width() // 2 - start_text.get_width() // 2,
                tile_y + tile_1.get_height() + 20
            ))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    running = False

    def show_decision_screen(self, game, ask_less=False):
        self.screen.fill((0, 0, 0))
        font = self.font
        decision_text = f"Which planet has {'less' if ask_less else 'more'} mushrooms, you believe?"
        decision_surface = font.render(decision_text, True, (255, 255, 255))
        current_world_image = visualize_wave_function(
            game.wave_function,
            game.player_pos,
            (GRID_ROWS, GRID_COLS),
            game.tile_surfaces,
            game.tile_names,
            ZOOM_FACTOR
        )
        image_x = (SCREEN_WIDTH - current_world_image.get_width()) // 2
        image_y = (SCREEN_HEIGHT // 5) - current_world_image.get_height() // 2  # Center it more vertically
        self.screen.blit(current_world_image, (image_x, image_y))
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Semi-transparent black overlay
        self.screen.blit(overlay, (0, 0))
        text_y = image_y + current_world_image.get_height() + 20
        self.screen.blit(decision_surface, (SCREEN_WIDTH // 2 - decision_surface.get_width() // 2, text_y))
        choice_1_text = "Planet 1: "
        choice_1_key = "[1]"
        choice_2_text = "Planet 2: "
        choice_2_key = "[2]"
        choice_1_surface = font.render(choice_1_text, True, (255, 255, 255))
        choice_1_key_surface = font.render(choice_1_key, True, (0, 255, 0))  # Green
        choice_2_surface = font.render(choice_2_text, True, (255, 255, 255))
        choice_2_key_surface = font.render(choice_2_key, True, (0, 255, 0))  # Green
        choices_y = text_y + 50  # Add spacing below the decision text
        choice_1_x = SCREEN_WIDTH // 2 - (choice_1_surface.get_width() + choice_1_key_surface.get_width()) // 2
        choice_2_x = SCREEN_WIDTH // 2 - (choice_2_surface.get_width() + choice_2_key_surface.get_width()) // 2
        self.screen.blit(choice_1_surface, (choice_1_x, choices_y))
        self.screen.blit(choice_1_key_surface, (choice_1_x + choice_1_surface.get_width(), choices_y))
        self.screen.blit(choice_2_surface, (choice_2_x, choices_y + 40))
        self.screen.blit(choice_2_key_surface, (choice_2_x + choice_2_surface.get_width(), choices_y + 40))
        label_font = pygame.font.Font(None, 36)
        label_text = f"Planet {game.world_id}"  # Current world ID
        label_surface = label_font.render(label_text, True, (255, 255, 255))  # White text
        label_width = label_surface.get_width() + 20  # Add padding
        label_height = label_surface.get_height() + 10
        pygame.draw.rect(
            self.screen,
            (50, 50, 50),  # Gray background for the label
            (10, 10, label_width, label_height)
        )
        self.screen.blit(label_surface, (20, 15))  # Adjusted padding for text placement
        pygame.display.flip()
        player_choice = self._get_player_choice()
        confidence = self.show_confidence_screen(game)
        self._clear_screen_with_game_background(game)
        return player_choice, confidence

    def show_confidence_screen(self, game):
        slider_width = 300
        slider_height = 10
        slider_x = SCREEN_WIDTH // 2 - slider_width // 2
        slider_y = SCREEN_HEIGHT // 2  # Positioned similar to the decision screen
        handle_radius = 10
        handle_x = slider_x  # Initially set to the left of the slider
        dragging = False  # Track if the handle is being dragged
        confidence = 0  # Confidence value (0-100)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if (event.pos[0] - handle_x) ** 2 + (event.pos[1] - slider_y) ** 2 <= handle_radius ** 2:
                        dragging = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    dragging = False
                elif event.type == pygame.MOUSEMOTION and dragging:
                    handle_x = max(slider_x, min(slider_x + slider_width, event.pos[0]))
                    confidence = int((handle_x - slider_x) / slider_width * 100)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    return confidence
            self.screen.fill((0, 0, 0))  # Clear the screen
            current_world_image = visualize_wave_function(
                game.wave_function,
                game.player_pos,
                (GRID_ROWS, GRID_COLS),
                game.tile_surfaces,
                game.tile_names,
                ZOOM_FACTOR
            )
            image_x = (SCREEN_WIDTH - current_world_image.get_width()) // 2
            image_y = (SCREEN_HEIGHT - current_world_image.get_height()) // 2
            self.screen.blit(current_world_image, (image_x, image_y))
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))  # Semi-transparent black (200/255 alpha)
            self.screen.blit(overlay, (0, 0))
            font = self.font
            confidence_text = font.render("How confident are you in your choice?", True, (255, 255, 255))
            confidence_level = font.render(f"Confidence: {confidence} per cent", True, (255, 255, 255))
            instructions = font.render("Press ENTER to continue", True, (255, 255, 255))
            text_x = SCREEN_WIDTH // 2 - confidence_text.get_width() // 2
            text_y = SCREEN_HEIGHT // 3
            self.screen.blit(confidence_text, (text_x, text_y))
            self.screen.blit(confidence_level, (SCREEN_WIDTH // 2 - confidence_level.get_width() // 2, slider_y + 40))
            self.screen.blit(instructions, (SCREEN_WIDTH // 2 - instructions.get_width() // 2, SCREEN_HEIGHT - 80))
            pygame.draw.rect(self.screen, (200, 200, 200), (slider_x, slider_y - slider_height // 2, slider_width, slider_height))
            pygame.draw.circle(self.screen, (255, 0, 0), (handle_x, slider_y), handle_radius)
            pygame.display.flip()

    def show_switch_instructions_screen(self, game1, game2, decision, conf):
        self.screen.fill((0, 0, 0))  # Clears the screen
        current_world_image = visualize_wave_function(
            game1.wave_function if game1.world_id == 1 else game2.wave_function,
            game1.player_pos if game1.world_id == 1 else game2.player_pos,
            (GRID_ROWS, GRID_COLS),
            game1.tile_surfaces if game1.world_id == 1 else game2.tile_surfaces,
            game1.tile_names if game1.world_id == 1 else game2.tile_names,
            ZOOM_FACTOR
        )
        image_x = (SCREEN_WIDTH - current_world_image.get_width()) // 2
        image_y = (SCREEN_HEIGHT - current_world_image.get_height()) // 2
        self.screen.blit(current_world_image, (image_x, image_y))
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  
        self.screen.blit(overlay, (0, 0))
        label_font = pygame.font.Font(None, 36)
        label_text = f"Planet {game1.world_id if game1.world_id == 1 else game2.world_id}"
        label_surface = label_font.render(label_text, True, (255, 255, 255))
        pygame.draw.rect(self.screen, (50, 50, 50), (10, 10, label_surface.get_width() + 20, label_surface.get_height() + 10))
        self.screen.blit(label_surface, (20, 15))
        overlay_height = 200
        bottom_overlay = pygame.Surface((SCREEN_WIDTH, overlay_height))
        bottom_overlay.fill((0, 0, 0))
        self.screen.blit(bottom_overlay, (0, SCREEN_HEIGHT - overlay_height))
        font = self.font
        text_lines = [
            f"Your choice was planet {int(decision)} (confidence: {int(conf)})",
            f"Now explore both planets freely in 50 steps"
        ]
        start_y = SCREEN_HEIGHT - overlay_height + 20
        line_spacing = 40
        for i, line in enumerate(text_lines):
            rendered_text = font.render(line, True, (255, 255, 255))
            text_x = (SCREEN_WIDTH - rendered_text.get_width()) // 2
            text_y = start_y + i * line_spacing
            self.screen.blit(rendered_text, (text_x, text_y))
        switch_text = "Press "
        planet_1_text = "[1]"
        middle_text = " for Planet 1, "
        planet_2_text = "[2]"
        end_text = " for Planet 2"
        switch_surface = font.render(switch_text, True, (255, 255, 255))
        planet_1_surface = font.render(planet_1_text, True, (0, 255, 0))  # Green
        middle_surface = font.render(middle_text, True, (255, 255, 255))
        planet_2_surface = font.render(planet_2_text, True, (0, 255, 0))  # Green
        end_surface = font.render(end_text, True, (255, 255, 255))
        combined_width = (
            switch_surface.get_width() +
            planet_1_surface.get_width() +
            middle_surface.get_width() +
            planet_2_surface.get_width() +
            end_surface.get_width()
        )
        text_x = (SCREEN_WIDTH - combined_width) // 2
        text_y = start_y + len(text_lines) * line_spacing
        self.screen.blit(switch_surface, (text_x, text_y))
        text_x += switch_surface.get_width()
        self.screen.blit(planet_1_surface, (text_x, text_y))
        text_x += planet_1_surface.get_width()
        self.screen.blit(middle_surface, (text_x, text_y))
        text_x += middle_surface.get_width()
        self.screen.blit(planet_2_surface, (text_x, text_y))
        text_x += planet_2_surface.get_width()
        self.screen.blit(end_surface, (text_x, text_y))
        switch_info_text = "You can switch anytime you want."
        switch_info_surface = font.render(switch_info_text, True, (255, 255, 255))
        switch_info_x = (SCREEN_WIDTH - switch_info_surface.get_width()) // 2
        switch_info_y = text_y + line_spacing  # Position below switch instructions
        self.screen.blit(switch_info_surface, (switch_info_x, switch_info_y))
        pygame.display.flip()
        chosen_world = self._get_player_choice()
        if chosen_world == 1:
            return game1
        elif chosen_world == 2:
            return game2# store this or is it clear in logfiles?
        
    def render_switch_instructions(self):
        font = self.font
        switch_text = "Press "
        planet_1_text = "[1]"
        middle_text = " for Planet 1, "
        planet_2_text = "[2]"
        end_text = " for Planet 2"
        switch_surface = font.render(switch_text, True, (255, 255, 255))
        planet_1_surface = font.render(planet_1_text, True, (0, 255, 0))  # Green
        middle_surface = font.render(middle_text, True, (255, 255, 255))
        planet_2_surface = font.render(planet_2_text, True, (0, 255, 0))  # Green
        end_surface = font.render(end_text, True, (255, 255, 255))
        combined_width = (
            switch_surface.get_width() +
            planet_1_surface.get_width() +
            middle_surface.get_width() +
            planet_2_surface.get_width() +
            end_surface.get_width()
        )
        text_x = (SCREEN_WIDTH - combined_width) // 2
        text_y = SCREEN_HEIGHT - 50  # Position near the bottom
        self.screen.blit(switch_surface, (text_x, text_y))
        text_x += switch_surface.get_width()
        self.screen.blit(planet_1_surface, (text_x, text_y))
        text_x += planet_1_surface.get_width()
        self.screen.blit(middle_surface, (text_x, text_y))
        text_x += middle_surface.get_width()
        self.screen.blit(planet_2_surface, (text_x, text_y))
        text_x += planet_2_surface.get_width()
        self.screen.blit(end_surface, (text_x, text_y))

    def show_transition_to_world_2_screen(self, game):
        current_world_image = visualize_wave_function(
            game.wave_function,
            game.player_pos,
            (GRID_ROWS, GRID_COLS),
            game.tile_surfaces,
            game.tile_names,
            ZOOM_FACTOR
        )
        image_x = (SCREEN_WIDTH - current_world_image.get_width()) // 2
        image_y = (SCREEN_HEIGHT - current_world_image.get_height()) // 2
        self.screen.blit(current_world_image, (image_x, image_y))
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Semi-transparent black
        self.screen.blit(overlay, (0, 0))
        overlay_height = 150  # Height of the black box
        bottom_overlay = pygame.Surface((SCREEN_WIDTH, overlay_height))
        bottom_overlay.fill((0, 0, 0))  # Solid black background
        self.screen.blit(bottom_overlay, (0, SCREEN_HEIGHT - overlay_height))
        font = self.font
        main_text = font.render("Now take 50 steps on planet 2", True, (255, 255, 255))
        main_text_x = (SCREEN_WIDTH - main_text.get_width()) // 2
        main_text_y = SCREEN_HEIGHT - overlay_height + 20
        self.screen.blit(main_text, (main_text_x, main_text_y))
        final_text = font.render("Press ENTER to continue...", True, (255, 255, 255))
        final_text_x = (SCREEN_WIDTH - final_text.get_width()) // 2
        final_text_y = main_text_y + 40  # Spaced below the main text
        self.screen.blit(final_text, (final_text_x, final_text_y))
        pygame.display.flip()
        self._wait_for_key(pygame.K_RETURN)

    def show_final_screen(self, stats, decisions):
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 24)  # Adjust font size for readability
        y_offset = 40
        for trial_num in range(NUM_TRIALS):
            prob_1, prob_2 = PROBABILITIES[trial_num]
            correct_world = 1 if prob_1 > prob_2 else 2  # Determine the correct world
            steps_1 = stats[0, 0, trial_num]
            steps_2 = stats[0, 1, trial_num]
            stones_1 = stats[1, 0, trial_num]
            stones_2 = stats[1, 1, trial_num]
            trial_decisions = decisions[trial_num, :]
            row_text = f"Trial {trial_num + 1}: {prob_1:.2f}:{prob_2:.2f} -- Steps: "
            rendered_text = font.render(row_text, True, (255, 255, 255))
            self.screen.blit(rendered_text, (20, trial_num * y_offset + 20))
            x_offset = 20 + rendered_text.get_width()
            for step1, step2 in zip(steps_1, steps_2):
                step1_surface = font.render(f"{int(step1)}", True, (0, 0, 255) if step1 > step2 else (255, 255, 255))
                self.screen.blit(step1_surface, (x_offset, trial_num * y_offset + 20))
                x_offset += step1_surface.get_width()
                colon_surface = font.render(":", True, (255, 255, 255))  # Render ":" in white
                self.screen.blit(colon_surface, (x_offset, trial_num * y_offset + 20))
                x_offset += colon_surface.get_width()
                step2_surface = font.render(f"{int(step2)}", True, (0, 0, 255) if step2 > step1 else (255, 255, 255))
                self.screen.blit(step2_surface, (x_offset, trial_num * y_offset + 20))
                x_offset += step2_surface.get_width()
            stones_label = font.render(" | Stones: ", True, (255, 255, 255))
            self.screen.blit(stones_label, (x_offset, trial_num * y_offset + 20))
            x_offset += stones_label.get_width()
            for stone1, stone2 in zip(stones_1, stones_2):
                stone1_surface = font.render(f"{int(stone1)}", True, (0, 0, 255) if stone1 > stone2 else (255, 255, 255))
                self.screen.blit(stone1_surface, (x_offset, trial_num * y_offset + 20))
                x_offset += stone1_surface.get_width()
                colon_surface = font.render(":", True, (255, 255, 255))  # Render ":" in white
                self.screen.blit(colon_surface, (x_offset, trial_num * y_offset + 20))
                x_offset += colon_surface.get_width()
                stone2_surface = font.render(f"{int(stone2)}", True, (0, 0, 255) if stone2 > stone1 else (255, 255, 255))
                self.screen.blit(stone2_surface, (x_offset, trial_num * y_offset + 20))
                x_offset += stone2_surface.get_width()
            decision_label = font.render(" | Decision: ", True, (255, 255, 255))
            self.screen.blit(decision_label, (x_offset, trial_num * y_offset + 20))
            x_offset += decision_label.get_width()
            for decision in trial_decisions:
                color = (0, 255, 0) if decision == correct_world else (255, 0, 0)  # Green for correct, red for incorrect
                decision_surface = font.render(str(int(decision)), True, color)
                self.screen.blit(decision_surface, (x_offset, trial_num * y_offset + 20))
                x_offset += decision_surface.get_width() + 5  # Add spacing between decisions
        font = self.font
        instruction_text = font.render("Press any key to exit", True, (255, 255, 255))
        self.screen.blit(instruction_text, (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2, SCREEN_HEIGHT - 50))
        pygame.display.flip()
        pygame.image.save(self.screen, "final_screen.png")
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Handle window close
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:  # Handle key press
                    waiting = False

    def _clear_screen_with_game_background(self, game):
        self.screen.fill((0, 0, 0))  # Clear screen
        current_world_image = visualize_wave_function(
            game.wave_function,
            game.player_pos,
            (GRID_ROWS, GRID_COLS),
            game.tile_surfaces,
            game.tile_names,
            ZOOM_FACTOR
        )
        image_x = (SCREEN_WIDTH - current_world_image.get_width()) // 2
        image_y = (SCREEN_HEIGHT - current_world_image.get_height()) // 2
        self.screen.blit(current_world_image, (image_x, image_y))
        pygame.display.flip()

    def _wait_for_key(self, key=None):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN and (key is None or event.key == key):
                    waiting = False

    def _get_player_choice(self):
        waiting = True
        choice = None
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        choice = 1
                        waiting = False
                    elif event.key == pygame.K_2:
                        choice = 2
                        waiting = False
        return choice
