import pygame
from enum import Enum

class AnimationState(Enum):
"Added five specific game states with this class"
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

"Not done yet!"
