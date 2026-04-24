
#axel m
import pygame

pygame.init()

debug_mode = True


screen = pygame.display.set_mode((1280, 720))

running = True

'''platforms = [
]'''

#floor_rect = pygame.Rect(0,610,1280,200)

clock = pygame.time.Clock()

x = 0
y = 0

vely = 0
gravity = 0.3

'''char = pygame.image.load("char.png")
char = pygame.transform.scale(char, (char.get_width()*.1, char.get_height()*.1))'''

background = pygame.image.load("Background.png")
background = pygame.transform.scale(background, (background.get_width()*2.5, background.get_height()*2.5))

on_ground = False

while running:
    screen.fill((0,0,0))
    screen.blit(background, (0, 0))
    #screen.blit(char, (x, y))
    #x += 1

    vely = gravity + vely
    y = vely + y

    #char_rect = char.get_rect(topleft=(x,y))

    '''for platform in platforms:

        if char_rect.colliderect(platform):
            y = platform.top - char_rect.height
            if vy < 0:
                y = platform.bottom
                vy = 0
            if x == platform.left:
                x = platform.left - char_rect.width
            if x == platform.right:
                x = platform.right
            vy = 0
            on_ground = True

    if debug_mode == True:
        pygame.draw.rect(screen, (255 ,0, 0), char_rect, 2)
        for platform in platforms:
            pygame.draw.rect(screen, (255 ,0, 0), platform, 2)'''

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                y = y-10

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and (on_ground == True):
        vy = -8
    if keys[pygame.K_DOWN]:
        y = y+3
    if keys[pygame.K_DOWN] and (on_ground == False):
        y = y + 10
    if keys[pygame.K_LEFT]:
        x = x-3
    if keys[pygame.K_RIGHT]:
        x = x+3
    on_ground = False

    if char_rect.colliderect(floor):
        y = floor.top - char_rect.height
        vy = 0
        on_ground = True

    clock.tick(30)

    pygame.display.flip()

pygame.quit()
