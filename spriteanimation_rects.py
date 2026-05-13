import pygame
from enum import Enum


class AnimationState(Enum):
    IDLE = "idle"
    WALK = "walk"
    RUN = "run"
    JUMP = "jump"
    GUARD = "guard"
    HIT = "hit"


class CharacterAnimator:
    """
    Rectangle-based animator for messy sprite sheets.

    This works better than row/column cutting because your sprite sheet is NOT
    evenly spaced. Each pygame.Rect tells pygame exactly what part to crop.
    """

    def __init__(self, sprite_sheet_path, scale=2):
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.scale = scale

        self.animations = {}
        self.speeds = {}

        self.current_state = AnimationState.IDLE
        self.current_frame = 0
        self.frame_counter = 0
        self.facing_right = True
        self.current_image = None

    def add_animation(self, state, rects, speed=6):
        """
        state = AnimationState.IDLE, WALK, etc.
        rects = list of pygame.Rect boxes
        speed = bigger number means slower animation
        """
        frames = []

        for rect in rects:
            frame = self.sprite_sheet.subsurface(rect).copy()

            if self.scale != 1:
                new_size = (
                    int(rect.width * self.scale),
                    int(rect.height * self.scale)
                )
                frame = pygame.transform.scale(frame, new_size)

            frames.append(frame)

        self.animations[state] = frames
        self.speeds[state] = speed

        if self.current_image is None and frames:
            self.current_image = frames[0]

    def set_state(self, new_state):
        """Change animation and restart from frame 0."""
        if new_state != self.current_state:
            self.current_state = new_state
            self.current_frame = 0
            self.frame_counter = 0

    def update(self):
        """Moves to the next frame when enough time has passed."""
        frames = self.animations.get(self.current_state)

        if not frames:
            return

        self.frame_counter += 1
        speed = self.speeds.get(self.current_state, 6)

        if self.frame_counter >= speed:
            self.frame_counter = 0
            self.current_frame = (self.current_frame + 1) % len(frames)

        image = frames[self.current_frame]

        if not self.facing_right:
            image = pygame.transform.flip(image, True, False)

        self.current_image = image

    def draw(self, surface, x, y):
        """Draw the current frame on the screen."""
        if self.current_image:
            surface.blit(self.current_image, (x, y))


def load_zeldris_animations(animator):
    """
    These rectangles are for the sprite sheet you showed me.

    Format:
    pygame.Rect(x, y, width, height)

    If one frame looks cut off, adjust its x/y/width/height a little.
    """

    # Top-left idle row
    animator.add_animation(AnimationState.IDLE, [
        pygame.Rect(10, 22, 29, 46),
        pygame.Rect(51, 22, 29, 46),
        pygame.Rect(96, 22, 29, 46),
    ], speed=10)

    # Stance row
    animator.add_animation(AnimationState.GUARD, [
        pygame.Rect(12, 224, 20, 46),
        pygame.Rect(44, 225, 20, 45),
    ], speed=10)

    # Walk row
    animator.add_animation(AnimationState.WALK, [
        pygame.Rect(14, 291, 19, 45),
        pygame.Rect(39, 291, 21, 45),
        pygame.Rect(68, 291, 22, 45),
        pygame.Rect(96, 291, 22, 45),
        pygame.Rect(151, 292, 21, 44),
        pygame.Rect(182, 292, 21, 44),
        pygame.Rect(210, 292, 21, 44),
        pygame.Rect(239, 292, 21, 44),
    ], speed=5)

    # Run/dash frames from the walk area
    animator.add_animation(AnimationState.RUN, [
        pygame.Rect(287, 300, 46, 31),
        pygame.Rect(336, 300, 45, 31),
    ], speed=4)

    # Jump row
    animator.add_animation(AnimationState.JUMP, [
        pygame.Rect(14, 363, 25, 47),
        pygame.Rect(50, 363, 28, 47),
        pygame.Rect(95, 356, 31, 54),
        pygame.Rect(133, 356, 31, 54),
        pygame.Rect(169, 350, 54, 60),
    ], speed=7)

    # Hit row
    animator.add_animation(AnimationState.HIT, [
        pygame.Rect(17, 482, 28, 48),
        pygame.Rect(64, 481, 29, 49),
        pygame.Rect(108, 483, 28, 47),
    ], speed=7)


# Example setup:
#
# pygame.init()
# screen = pygame.display.set_mode((900, 600))
# clock = pygame.time.Clock()
#
# player = CharacterAnimator("sprites_de__zeldris_jus_hd_by_rakionmugen1_ddxuxdn.png", scale=2)
# load_zeldris_animations(player)
#
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#
#     keys = pygame.key.get_pressed()
#
#     if keys[pygame.K_RIGHT]:
#         player.facing_right = True
#         player.set_state(AnimationState.WALK)
#     elif keys[pygame.K_LEFT]:
#         player.facing_right = False
#         player.set_state(AnimationState.WALK)
#     elif keys[pygame.K_SPACE]:
#         player.set_state(AnimationState.JUMP)
#     else:
#         player.set_state(AnimationState.IDLE)
#
#     player.update()
#
#     screen.fill((112, 146, 190))
#     player.draw(screen, 300, 300)
#     pygame.display.flip()
#     clock.tick(60)
#
# pygame.quit()
