import pygame
from enum import Enum

class AnimationState(Enum):
"5 different game states"
        IDLE = 0
        WALK = 1
        RUN = 2
        ATTACK = 3
        JUMP = 4

class CharacterAnimator:
"Handles sprite animation and frame control"
        def __init__(self, sprite_sheet_path, frame_width, frame_height, scale=2):
            "Gives access to sprite sheet files + allows to adjust framewdith, height, and scale"

            self.sprite_sheet = pygame.image.load(sprite_sheet_path)
            self.frame_width = frame_width
            self.frame_height = frame_height
            self.scale = scale

            "Starting Animation State"
            self.current_state = AnimationState.IDLE
            self.current_frame = 0
            self.frame_counter = 0

            "Animation Settings"
            self.animations = {} "Stores lists of frames per state"
            self.animation_speed = 5 "The lower the number, the faster the animation"

            "Character direction and rendering"
            self.facing_right = True
            self.current_image = None

            "Starts the first frame"
            self.update_frame()

        def add_animation(self, state, row, frame_count, speed = None):
            "Add an animation state to the editor HERE"

            "Breakdown:"
                "state: AnimationState enum value"
                "row: Which row in the sprite sheet"
                "frame_count: How many frames in this animation"
                "speed: Animation speed"

            def extract_frame(self, row, col):
                "This is gonna extract a single frame from the sprite sheet"

                src_rect = pygame.Rect(
                    col * self.frame_width,
                    row * self.frame_height,
                    self.frame_width,
                    self.frame_height
                )
                frame =
            self.sprite_sheet.subsurface(src_rect).copy()
                return frame
