import pygame
from enum import Enum


class AnimationState(Enum):
    IDLE = "idle"
    WALK = "walk"
    RUN = "run"
    JUMP = "jump"
    GUARD = "guard"
    HIT = "hit"
    ULTIMATE = "ultimate"
    B = "b"
    UP_B = "up_b"
    DOWN_B = "down_b"
    AERIAL_B = "aerial_b"
    Y = "y"
    FORWARD_Y = "forward_y"
    UP_Y = "up_y"
    DOWN_Y = "down_y"
    AERIAL_Y = "aerial_y"
    X = "x"
    X_UP = "x_up"
    HURT = "hurt"
    WIN = "win"
    LOSE = "lose"


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


def load_rias_animations(animator):
    """
    Rectangles mapped from Fried.png (1360x1632).
    Format: pygame.Rect(x, y, width, height)

    Note: IDLE is mapped to STANCE frames (the idle loop).
          WALK is mapped to RUN frames (closest equivalent).
    """

    # STANCE — idle loop (4 frames)
    animator.add_animation(AnimationState.IDLE, [
        pygame.Rect(6,   24, 30, 46),
        pygame.Rect(53,  24, 30, 46),
        pygame.Rect(96,  24, 32, 46),
        pygame.Rect(142, 24, 31, 47),
    ], speed=10)

    # RUN (6 frames)
    animator.add_animation(AnimationState.RUN, [
        pygame.Rect(2,   96, 42, 45),
        pygame.Rect(51,  96, 42, 45),   # trimmed merged group; adjust if needed
        pygame.Rect(175, 96, 35, 45),
        pygame.Rect(217, 96, 42, 45),
        pygame.Rect(271, 96, 38, 45),
        pygame.Rect(319, 96, 33, 45),
    ], speed=5)

    # WALK — reuse RUN frames (no separate walk row on this sheet)
    animator.add_animation(AnimationState.WALK, [
        pygame.Rect(2,   96, 42, 45),
        pygame.Rect(175, 96, 35, 45),
        pygame.Rect(217, 96, 42, 45),
        pygame.Rect(271, 96, 38, 45),
        pygame.Rect(319, 96, 33, 45),
    ], speed=7)

    # JUMP (7 frames)
    animator.add_animation(AnimationState.JUMP, [
        pygame.Rect(13,  186, 28, 41),
        pygame.Rect(53,  174, 50, 53),  # wide group split; first half
        pygame.Rect(160, 171, 50, 56),  # second half of that group
        pygame.Rect(278, 171, 41, 56),
        pygame.Rect(329, 186, 41, 41),
        pygame.Rect(377, 194, 31, 34),
        pygame.Rect(415, 186, 28, 41),
    ], speed=7)

    # GUARD (3 frames)
    animator.add_animation(AnimationState.GUARD, [
        pygame.Rect(14, 257, 32, 45),
        pygame.Rect(57, 258, 33, 43),
        pygame.Rect(97, 255, 31, 44),
    ], speed=10)

    # ULTIMATE ACTION (3 frames)
    animator.add_animation(AnimationState.ULTIMATE, [
        pygame.Rect(13, 331, 28, 51),
        pygame.Rect(54, 331, 26, 51),
        pygame.Rect(92, 332, 39, 50),
    ], speed=8)

    # B attack (4 frames)
    animator.add_animation(AnimationState.B, [
        pygame.Rect(14,  413, 31, 45),
        pygame.Rect(57,  416, 50, 42),
        pygame.Rect(118, 416, 48, 42),
        pygame.Rect(179, 414, 37, 44),
    ], speed=6)

    # UP + B (2 frames)
    animator.add_animation(AnimationState.UP_B, [
        pygame.Rect(17, 487, 25, 47),
        pygame.Rect(58, 489, 48, 45),
    ], speed=6)

    # DOWN + B (2 frames)
    animator.add_animation(AnimationState.DOWN_B, [
        pygame.Rect(9,   576, 80, 50),  # wide group — split roughly in half
        pygame.Rect(95,  576, 80, 50),
        pygame.Rect(184, 576, 28, 50),
    ], speed=6)

    # AERIAL B (4 frames)
    animator.add_animation(AnimationState.AERIAL_B, [
        pygame.Rect(17,  672, 28, 40),
        pygame.Rect(56,  663, 31, 47),
        pygame.Rect(96,  678, 31, 34),
        pygame.Rect(134, 670, 28, 41),
    ], speed=6)

    # Y attack (4 frames)
    animator.add_animation(AnimationState.Y, [
        pygame.Rect(13,  752, 33, 44),
        pygame.Rect(56,  755, 50, 41),
        pygame.Rect(114, 755, 50, 41),
        pygame.Rect(176, 753, 35, 43),
    ], speed=6)

    # FORWARD + Y (4 frames)
    animator.add_animation(AnimationState.FORWARD_Y, [
        pygame.Rect(4,   837, 26, 50),
        pygame.Rect(69,  836, 22, 48),
        pygame.Rect(124, 836, 25, 49),
        pygame.Rect(190, 833, 45, 49),
    ], speed=6)

    # UP + Y (6 frames)
    animator.add_animation(AnimationState.UP_Y, [
        pygame.Rect(21,  928, 30, 38),
        pygame.Rect(59,  936, 41, 30),
        pygame.Rect(116, 916, 38, 51),
        pygame.Rect(163, 916, 38, 53),
        pygame.Rect(228, 918, 34, 47),
        pygame.Rect(292, 928, 44, 30),
    ], speed=6)

    # DOWN + Y (6 frames)
    animator.add_animation(AnimationState.DOWN_Y, [
        pygame.Rect(16,  1013, 30, 38),
        pygame.Rect(54,  1021, 41, 31),
        pygame.Rect(111, 1000, 60, 52),  # wide group split
        pygame.Rect(175, 1000, 60, 52),
        pygame.Rect(255, 1003, 69, 49),
        pygame.Rect(341, 1006, 47, 47),
        pygame.Rect(401, 1016, 44, 30),
    ], speed=6)

    # AERIAL Y (5 frames)
    animator.add_animation(AnimationState.AERIAL_Y, [
        pygame.Rect(14,  1090, 38, 50),
        pygame.Rect(61,  1090, 31, 54),
        pygame.Rect(101, 1090, 39, 50),
        pygame.Rect(160, 1091, 44, 50),
        pygame.Rect(224, 1091, 33, 41),
    ], speed=6)

    # X attack (2 frames — second is a wide swipe effect)
    animator.add_animation(AnimationState.X, [
        pygame.Rect(18, 1196, 30,  48),
        pygame.Rect(56, 1195, 110, 50),
    ], speed=6)

    # X + UP (3 frames)
    animator.add_animation(AnimationState.X_UP, [
        pygame.Rect(20,  1297, 25, 51),
        pygame.Rect(70,  1288, 28, 62),
        pygame.Rect(114, 1291, 25, 58),
    ], speed=6)

    # HIT — use first 5 clean frames (rest are fall/getup)
    animator.add_animation(AnimationState.HIT, [
        pygame.Rect(6,   1425, 32, 50),
        pygame.Rect(52,  1427, 34, 42),
        pygame.Rect(92,  1423, 78, 47),
        pygame.Rect(176, 1433, 51, 26),
        pygame.Rect(236, 1432, 37, 33),
    ], speed=7)

    # WIN (character + heart burst — first 2 are character frames)
    animator.add_animation(AnimationState.WIN, [
        pygame.Rect(21,  1508, 30, 48),
        pygame.Rect(60,  1508, 30, 48),
        pygame.Rect(180, 1516, 28, 27),
    ], speed=10)

    # LOSE (2 frames)
    animator.add_animation(AnimationState.LOSE, [
        pygame.Rect(27, 1580, 41, 41),
        pygame.Rect(75, 1588, 31, 34),
    ], speed=10)


# Example setup:
#
# pygame.init()
# screen = pygame.display.set_mode((900, 600))
# clock = pygame.time.Clock()
#
# player = CharacterAnimator("Fried.png", scale=2)
# load_rias_animations(player)
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
#     screen.fill((30, 30, 50))
#     player.draw(screen, 300, 300)
#     pygame.display.flip()
#     clock.tick(60)
#
# pygame.quit()
