import pygame
import spriteanimation as anims

charList = [
    Zeldras,
    MD
]

input = pygame.key.get_pressed()

class Characters:
    def __init__(char, moves, img):
        char.moves = moves
        char.img = img

    def getChar:
