#axel m, malem and fernando
import pygame

pygame.init()

debug_mode = False

screen = pygame.display.set_mode((1280, 720))

running = True

clock = pygame.time.Clock()

x = 50
y = 50

x2 = 300 # second player
y2 = 300 # second player

vy = 0
vy2 = 0 # second player
gravity = 0.4

#Using generic names like "char" and "background" as we will have multiple of these

char = pygame.image.load("IdleZeldras.png") #Temporarily using just IdleZeldras.png as we find a way to implement character's animations
char = pygame.transform.scale(char, (char.get_width()*2, char.get_height()*2))

char2 = pygame.image.load("IdleZeldras.png") #Temporarily using a less compact method to test multiple players
char2 = pygame.transform.flip(char2, True, False)
char2 = pygame.transform.scale(char2, (char2.get_width()*2, char2.get_height()*2))#This will get turned into a function later to possibly add more than 2 players

background = pygame.image.load("Background.png")
background = pygame.transform.scale(background, (background.get_width()*2.5, background.get_height()*3.22))

on_ground = False
on_ground2 = False # second player

#By giving the background its own X and Y variables, we're able to make more creative maps that cna scroll left to right or up and down

bgX_width = background.get_width()
bgY_height = background.get_height()

bg_X = 0
bg_Y = 0

platforms = [
    pygame.Rect(0,610,bgX_width,200), # floor rectangle
    #pygame.Rect(0,-50, 1, 800), left border
    #pygame.Rect(1280,-50, 1, 800) right border
]

#Due to these having their own special effects on the game, they're seperate from other platforms
#Left Border and Right Border are seperate because they have to also account for the background being able to move

border_L = pygame.Rect(0,-50, 1, 800) #Rectangles are a bit larger than screen width to accomadate any accidental clipping during playtime
border_R = pygame.Rect(1280,-50, 1, 800)


while running:
    screen.blit(background, (bg_X, bg_Y))
    screen.blit(char, (x, y))
    '''screen.blit(char2, (x2, y2))'''# second player

    char_rect = char.get_rect(topleft=(x,y))
    '''char2_rect = char2.get_rect(topleft=(x2,y2))''' # second player

    vy = gravity + vy #modifies the rate of the player's descent while jumping
    '''vy2 = gravity + vy2''' # second player

    y = vy + y
    '''y2 = vy2 + y2''' # second player

    for platform in platforms:
        if char_rect.colliderect(platform):
            y = platform.top - char_rect.height
            if vy < 0:
                if platform == platform[0]:
                    y = platform.top - char_rect.height
                    vy = 0
                y = platform.bottom
                vy = 0
            if x == platform.left:
                '''if platform == platform[1]:
                    if bg_X >= ((bgX_width - bgX_width)): #(bgX_width - bgX_width) is a constant used to make the comparison work. The reason "0" isn't used is because this can provide a more specific value for the comparison
                        bg_X = -10 #We set bg_X to -10 as that's how much the player moves. Any less and the background would get a bit glitchy.
                    bg_X = bg_X + 10 #adds to the bg_X value to move left
                    x = platform[1].right
                x = platform.left - char_rect.width'''
            if x == platform.right:
                '''if platform == platform[2]:
                    if bg_X <= ((-bgX_width + 1280)):
                        bg_X = ((-bgX_width + 1280) + 10)
                    bg_X = bg_X - 10
                    x = platform[2].left - char_rect.width'''
                x = platform.right
            vy = 0
            on_ground = True
        '''if char2_rect.colliderect(platform): # second player
            y2 = platform.top - char2_rect.height
            if vy2 < 0:
                if platform == platform[0]:
                    y2 = platform.top - char2_rect.height
                    vy2 = 0
                y2 = platform.bottom
                vy2 = 0
            if x2 == platform.left:
                if platform == platform[1]:
                    if bg_X >= ((bgX_width - bgX_width)): #(bgX_width - bgX_width) is a constant used to make the comparison work. The reason "0" isn't used is because this can provide a more specific value for the comparison
                        bg_X = -10 #We set bg_X to -10 as that's how much the player moves. Any less and the background would get a bit glitchy.
                    bg_X = bg_X + 10 #adds to the bg_X value to move left
                    x2 = platform[1].right
                x2 = platform.left - char2_rect.width
            if x2 == platform.right:
                if platform == platform[2]:
                    if bg_X <= ((-bgX_width + 1280)):
                        bg_X = ((-bgX_width + 1280) + 10)
                    bg_X = bg_X - 10
                    x2 = platform[2].left - char_rect.width
                x2 = platform.right
            vy2 = 0
            on_ground2 = True'''

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

    '''if keys[pygame.K_w] and (on_ground2 == True): # second player
        vy2 = -8
    if keys[pygame.K_s]:
        y2 = y2+5
    if keys[pygame.K_s] and (on_ground2 == False):
        y2 = y2 + 10
    if keys[pygame.K_a]:
        x2 = x2-10
    if keys[pygame.K_d]:
        x2 = x2+10
    on_ground2 = False'''

    while debug_mode:
        pygame.draw.rect(screen, (255 ,0, 0), char_rect, 2)
        '''pygame.draw.rect(screen, (255 ,0, 0), char2_rect, 2)''' # second player
        for platform in platforms:
            pygame.draw.rect(screen, (255 ,0, 0), platform, 2)

    if char_rect.colliderect(border_L):
        if bg_X >= ((bgX_width - bgX_width)): #(bgX_width - bgX_width) is a constant used to make the comparison work. The reason "0" isn't used is because this can provide a more specific value for the comparison
            bg_X = -10 #We set bg_X to -10 as that's how much the player moves. Any less and the background would get a bit glitchy.
        bg_X = bg_X + 10 #adds to the bg_X value to move left
        x = border_L.right

    if char_rect.colliderect(border_R):
        if bg_X <= ((-bgX_width + 1280)):
            bg_X = ((-bgX_width + 1280) + 10)
        bg_X = bg_X - 10
        x = border_R.left - char_rect.width

    '''if char2_rect.colliderect(border_L): # second player
        if bg_X >= ((bgX_width - bgX_width)): #(bgX_width - bgX_width) is a constant used to make the comparison work. The reason "0" isn't used is because this can provide a more specific value for the comparison
            bg_X = -10 #
        bg_X = bg_X
        x2 = border_L.right

    if char2_rect.colliderect(border_R): # second player
        if bg_X <= ((-bgX_width + 1280)): #In progress
            bg_X = ((-bgX_width + 1280) + 10)
        bg_X = bg_X - 10
        x2 = border_R.left - char2_rect.width'''

    clock.tick(30)

    pygame.display.flip()

pygame.quit()
