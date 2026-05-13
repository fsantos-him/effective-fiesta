import pygame
from enum import Enum


class AnimationState(Enum):
    IDLE = "idle"
    WALK = "walk"
    RUN = "run"
    JUMP = "jump"
    GUARD = "guard"
    HIT = "hit"
    ATTACK = "attack"
    SPECIAL = "special"


class CharacterAnimator:
    """
    Rectangle-based animator for messy sprite sheets.

    This works better than row/column cutting because this sprite sheet is not
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
        state = AnimationState.IDLE, WALK, ATTACK, etc.
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
        """Moves to the next animation frame."""
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
        """Draw the current character frame."""
        if self.current_image:
            surface.blit(self.current_image, (x, y))


class AnimatedEffect:
    """
    This is for special attack effects, like the purple slash/blade.

    It is separate from the player because effects usually move, disappear,
    and hit enemies on their own.
    """

    def __init__(self, sprite_sheet_path, rects, x, y, facing_right=True, scale=2, speed=4, move_speed=8):
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.frames = []
        self.x = x
        self.y = y
        self.facing_right = facing_right
        self.speed = speed
        self.move_speed = move_speed

        self.current_frame = 0
        self.frame_counter = 0
        self.finished = False

        for rect in rects:
            frame = self.sprite_sheet.subsurface(rect).copy()

            if scale != 1:
                new_size = (
                    int(rect.width * scale),
                    int(rect.height * scale)
                )
                frame = pygame.transform.scale(frame, new_size)

            if not facing_right:
                frame = pygame.transform.flip(frame, True, False)

            self.frames.append(frame)

    def update(self):
        """Move the slash forward and animate it once."""
        if self.finished or not self.frames:
            return

        if self.facing_right:
            self.x += self.move_speed
        else:
            self.x -= self.move_speed

        self.frame_counter += 1

        if self.frame_counter >= self.speed:
            self.frame_counter = 0
            self.current_frame += 1

            if self.current_frame >= len(self.frames):
                self.finished = True

    def draw(self, surface):
        """Draw the current slash frame."""
        if not self.finished and self.frames:
            surface.blit(self.frames[self.current_frame], (self.x, self.y))

    def get_hitbox(self):
        """Rectangle used for collision/damage later."""
        if self.finished or not self.frames:
            return pygame.Rect(0, 0, 0, 0)

        image = self.frames[self.current_frame]
        return pygame.Rect(self.x, self.y, image.get_width(), image.get_height())


def load_zeldris_animations(animator):
    """
    These rectangles are estimated for the sprite sheet.

    Format:
    pygame.Rect(x, y, width, height)

    If a frame looks cut off, slightly adjust x, y, width, or height.
    """

    animator.add_animation(AnimationState.IDLE, [
        pygame.Rect(10, 22, 29, 46),
        pygame.Rect(51, 22, 29, 46),
        pygame.Rect(96, 22, 29, 46),
    ], speed=10)

    animator.add_animation(AnimationState.GUARD, [
        pygame.Rect(12, 224, 20, 46),
        pygame.Rect(44, 225, 20, 45),
    ], speed=10)

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

    animator.add_animation(AnimationState.RUN, [
        pygame.Rect(287, 300, 46, 31),
        pygame.Rect(336, 300, 45, 31),
    ], speed=4)

    animator.add_animation(AnimationState.JUMP, [
        pygame.Rect(14, 363, 25, 47),
        pygame.Rect(50, 363, 28, 47),
        pygame.Rect(95, 356, 31, 54),
        pygame.Rect(133, 356, 31, 54),
        pygame.Rect(169, 350, 54, 60),
    ], speed=7)

    animator.add_animation(AnimationState.HIT, [
        pygame.Rect(17, 482, 28, 48),
        pygame.Rect(64, 481, 29, 49),
        pygame.Rect(108, 483, 28, 47),
    ], speed=7)

    # Basic sword attack frames
    animator.add_animation(AnimationState.ATTACK, [
        pygame.Rect(15, 646, 29, 48),
        pygame.Rect(53, 646, 42, 48),
        pygame.Rect(101, 646, 38, 48),
    ], speed=5)

    # Special attack character startup frames
    animator.add_animation(AnimationState.SPECIAL, [
        pygame.Rect(14, 1216, 29, 48),
        pygame.Rect(55, 1216, 32, 48),
        pygame.Rect(100, 1216, 32, 48),
    ], speed=5)


def get_purple_slash_rects():
    """
    Purple blade/slash frames from the special attack area.

    These are estimates. If the slash is cut off, make the rectangles wider/taller.
    """
    return [
        pygame.Rect(270, 1009, 95, 92),
        pygame.Rect(350, 1006, 110, 102),
        pygame.Rect(425, 1000, 125, 115),
        pygame.Rect(500, 1008, 90, 95),
    ]


# -------------------- EXAMPLE GAME LOOP --------------------
#
# Put this in your main game file, not inside the class.
#
# pygame.init()
# screen = pygame.display.set_mode((900, 600))
# clock = pygame.time.Clock()
#
# SPRITE_SHEET = "sprites_de__zeldris_jus_hd_by_rakionmugen1_ddxuxdn.png"
#
# player = CharacterAnimator(SPRITE_SHEET, scale=2)
# load_zeldris_animations(player)
#
# player_x = 300
# player_y = 300
# effects = []
#
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_f:
#                 player.set_state(AnimationState.ATTACK)
#
#             if event.key == pygame.K_g:
#                 player.set_state(AnimationState.SPECIAL)
#
#                 # Spawn the purple blade in front of the player
#                 if player.facing_right:
#                     slash_x = player_x + 55
#                 else:
#                     slash_x = player_x - 170
#
#                 slash_y = player_y - 25
#
#                 effects.append(
#                     AnimatedEffect(
#                         SPRITE_SHEET,
#                         get_purple_slash_rects(),
#                         slash_x,
#                         slash_y,
#                         facing_right=player.facing_right,
#                         scale=2,
#                         speed=4,
#                         move_speed=10
#                     )
#                 )
#
#     keys = pygame.key.get_pressed()
#
#     if keys[pygame.K_RIGHT]:
#         player_x += 4
#         player.facing_right = True
#         player.set_state(AnimationState.WALK)
#     elif keys[pygame.K_LEFT]:
#         player_x -= 4
#         player.facing_right = False
#         player.set_state(AnimationState.WALK)
#     elif keys[pygame.K_SPACE]:
#         player.set_state(AnimationState.JUMP)
#     elif not keys[pygame.K_f] and not keys[pygame.K_g]:
#         player.set_state(AnimationState.IDLE)
#
#     player.update()
#
#     for effect in effects:
#         effect.update()
#
#     # Remove finished purple slashes
#     effects = [effect for effect in effects if not effect.finished]
#
#     screen.fill((112, 146, 190))
#     player.draw(screen, player_x, player_y)
#
#     for effect in effects:
#         effect.draw(screen)
#
#     pygame.display.flip()
#     clock.tick(60)
#
# pygame.quit()
