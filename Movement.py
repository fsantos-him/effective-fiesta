#axel m, malem and fernando
import pygame

pygame.init()

debug_mode = True

screen = pygame.display.set_mode((1280, 720))

running = True

platforms = [
    pygame.Rect(0,610,1280,200)
]

#Due to these having their own special effects on the game, they're seperate from other platforms
#Left Border and Right Border are seperate because they have to also account for the background being able to move

border_L = pygame.Rect(0,-50, 1, 800) #Rectangles are a bit larger than screen width to accomadate any accidental clipping during playtime
border_R = pygame.Rect(1280,-50, 1, 800)

clock = pygame.time.Clock()

#By giving the background its own X and Y variables, we're able to make more creative maps that cna scroll left to right or up and down

bg_Y = 0
bg_X = 0

x = 0
y = 0

vy = 0
gravity = 0.4

#Using generic names like "char" and "background" as we will have multiple of these

char = pygame.image.load("IdleZeldras.png") #Temporarily using just IdleZeldras.png as we find a way to implement character's animations
char = pygame.transform.scale(char, (char.get_width()*2, char.get_height()*2))

background = pygame.image.load("Background.png")
background = pygame.transform.scale(background, (background.get_width()*2.5, background.get_height()*3.22))

on_ground = False

while running:
    screen.blit(background, (bg_X, bg_Y))
    screen.blit(char, (x, y))

    char_rect = char.get_rect(topleft=(x,y))

    vy = gravity + vy #modifies the rate of the player's descent while jumping
    y = vy + y

    for platform in platforms:
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
            pygame.draw.rect(screen, (255 ,0, 0), platform, 2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

#Different movement options (Using arrow keys) with a jump and a special quick descent type move (when pressing down and off the ground) for fun
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and (on_ground == True):
        vy = -8
    if keys[pygame.K_DOWN]:
        y = y+5
    if keys[pygame.K_DOWN] and (on_ground == False):
        y = y + 10
    if keys[pygame.K_LEFT]:
        x = x-10
    if keys[pygame.K_RIGHT]:
        x = x+10
    on_ground = False

    if char_rect.colliderect(border_L):
        bg_X = bg_X + 10
        x = border_L.right

    if char_rect.colliderect(border_R):
        bg_X = bg_X - 10
        x = border_R.left - char_rect.width

    clock.tick(30)

    pygame.display.flip()

pygame.quit()
