import pygame
from enum import Enum


class AnimationState(Enum):
    # Shared
    IDLE      = "idle"
    WALK      = "walk"
    RUN       = "run"
    JUMP      = "jump"
    GUARD     = "guard"
    HIT       = "hit"
    WIN       = "win"
    LOSE      = "lose"
    # Rias-specific
    ULTIMATE  = "ultimate"
    B         = "b"
    UP_B      = "up_b"
    DOWN_B    = "down_b"
    AERIAL_B  = "aerial_b"
    Y         = "y"
    FORWARD_Y = "forward_y"
    UP_Y      = "up_y"
    DOWN_Y    = "down_y"
    AERIAL_Y  = "aerial_y"
    X         = "x"
    X_UP      = "x_up"


class CharacterAnimator:
    """
    Rectangle-based animator for messy sprite sheets.

    One instance per character:
        rias    = CharacterAnimator("Fried.png", scale=2)
        zeldris = CharacterAnimator("zeldris.png", scale=2)
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
        state = AnimationState enum value
        rects = list of pygame.Rect boxes
        speed = frames to wait before advancing (higher = slower)
        """
        frames = []

        for rect in rects:
            frame = self.sprite_sheet.subsurface(rect).copy()

            if self.scale != 1:
                new_size = (
                    int(rect.width  * self.scale),
                    int(rect.height * self.scale)
                )
                frame = pygame.transform.scale(frame, new_size)

            frames.append(frame)

        self.animations[state] = frames
        self.speeds[state] = speed

        if self.current_image is None and frames:
            self.current_image = frames[0]

    def set_state(self, new_state, fallback=AnimationState.IDLE):
        """
        Change animation and restart from frame 0.
        If this character has no frames for new_state, falls back to `fallback`
        so Zeldris won't break if given a Rias-only state.
        """
        if new_state not in self.animations:
            new_state = fallback
        if new_state != self.current_state:
            self.current_state = new_state
            self.current_frame = 0
            self.frame_counter = 0

    def update(self):
        """Advance to the next frame when enough time has passed."""
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
        """Draw the current frame at (x, y)."""
        if self.current_image:
            surface.blit(self.current_image, (x, y))


# ---------------------------------------------------------------------------
# RIAS  (Fried.png  —  1360 x 1632)
# ---------------------------------------------------------------------------

def load_rias_animations(animator):
    """
    Pixel-detected rects from Fried.png.
    Format: pygame.Rect(x, y, width, height)
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
        pygame.Rect(51,  96, 42, 45),
        pygame.Rect(175, 96, 35, 45),
        pygame.Rect(217, 96, 42, 45),
        pygame.Rect(271, 96, 38, 45),
        pygame.Rect(319, 96, 33, 45),
    ], speed=5)

    # WALK — reuses RUN frames (no separate walk row on this sheet)
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
        pygame.Rect(53,  174, 50, 53),
        pygame.Rect(160, 171, 50, 56),
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

    # DOWN + B (3 frames)
    animator.add_animation(AnimationState.DOWN_B, [
        pygame.Rect(9,   576, 80, 50),
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

    # DOWN + Y (7 frames)
    animator.add_animation(AnimationState.DOWN_Y, [
        pygame.Rect(16,  1013, 30, 38),
        pygame.Rect(54,  1021, 41, 31),
        pygame.Rect(111, 1000, 60, 52),
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

    # X attack (2 frames)
    animator.add_animation(AnimationState.X, [
        pygame.Rect(18, 1196,  30, 48),
        pygame.Rect(56, 1195, 110, 50),
    ], speed=6)

    # X + UP (3 frames)
    animator.add_animation(AnimationState.X_UP, [
        pygame.Rect(20,  1297, 25, 51),
        pygame.Rect(70,  1288, 28, 62),
        pygame.Rect(114, 1291, 25, 58),
    ], speed=6)

    # HIT — first 5 frames (rest are fall/getup)
    animator.add_animation(AnimationState.HIT, [
        pygame.Rect(6,   1425, 32, 50),
        pygame.Rect(52,  1427, 34, 42),
        pygame.Rect(92,  1423, 78, 47),
        pygame.Rect(176, 1433, 51, 26),
        pygame.Rect(236, 1432, 37, 33),
    ], speed=7)

    # WIN (3 frames — character only, before the heart burst)
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


# ---------------------------------------------------------------------------
# ZELDRIS  (sprites_de__zeldris_jus_hd_by_rakionmugen1_ddxuxdn.png)
# ---------------------------------------------------------------------------

def load_zeldris_animations(animator):
    """
    Rectangles for the Zeldris sprite sheet.
    Format: pygame.Rect(x, y, width, height)

    Zeldris only registers shared states (IDLE, WALK, RUN, JUMP, GUARD, HIT).
    Rias-specific states (B, Y, X, etc.) are not registered here — set_state()
    will automatically fall back to IDLE if those are ever called on him.
    """

    # IDLE (3 frames)
    animator.add_animation(AnimationState.IDLE, [
        pygame.Rect(10, 22, 29, 46),
        pygame.Rect(51, 22, 29, 46),
        pygame.Rect(96, 22, 29, 46),
    ], speed=10)

    # GUARD / STANCE (2 frames)
    animator.add_animation(AnimationState.GUARD, [
        pygame.Rect(12, 224, 20, 46),
        pygame.Rect(44, 225, 20, 45),
    ], speed=10)

    # WALK (8 frames)
    animator.add_animation(AnimationState.WALK, [
        pygame.Rect(14,  291, 19, 45),
        pygame.Rect(39,  291, 21, 45),
        pygame.Rect(68,  291, 22, 45),
        pygame.Rect(96,  291, 22, 45),
        pygame.Rect(151, 292, 21, 44),
        pygame.Rect(182, 292, 21, 44),
        pygame.Rect(210, 292, 21, 44),
        pygame.Rect(239, 292, 21, 44),
    ], speed=5)

    # RUN / DASH (2 frames)
    animator.add_animation(AnimationState.RUN, [
        pygame.Rect(287, 300, 46, 31),
        pygame.Rect(336, 300, 45, 31),
    ], speed=4)

    # JUMP (5 frames)
    animator.add_animation(AnimationState.JUMP, [
        pygame.Rect(14,  363, 25, 47),
        pygame.Rect(50,  363, 28, 47),
        pygame.Rect(95,  356, 31, 54),
        pygame.Rect(133, 356, 31, 54),
        pygame.Rect(169, 350, 54, 60),
    ], speed=7)

    # HIT (3 frames)
    animator.add_animation(AnimationState.HIT, [
        pygame.Rect(17,  482, 28, 48),
        pygame.Rect(64,  481, 29, 49),
        pygame.Rect(108, 483, 28, 47),
    ], speed=7)


# ---------------------------------------------------------------------------
# Example setup
# ---------------------------------------------------------------------------
#
# pygame.init()
# screen = pygame.display.set_mode((900, 600))
# clock  = pygame.time.Clock()
#
# rias = CharacterAnimator("Fried.png", scale=2)
# load_rias_animations(rias)
#
# zeldris = CharacterAnimator("zeldris.png", scale=2)
# load_zeldris_animations(zeldris)
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
#         rias.facing_right = True
#         rias.set_state(AnimationState.WALK)
#     elif keys[pygame.K_LEFT]:
#         rias.facing_right = False
#         rias.set_state(AnimationState.WALK)
#     elif keys[pygame.K_SPACE]:
#         rias.set_state(AnimationState.JUMP)
#     else:
#         rias.set_state(AnimationState.IDLE)
#
#     rias.update()
#     zeldris.update()
#
#     screen.fill((30, 30, 50))
#     rias.draw(screen, 200, 300)
#     zeldris.draw(screen, 600, 300)
#     pygame.display.flip()
#     clock.tick(60)
#
# pygame.quit()
