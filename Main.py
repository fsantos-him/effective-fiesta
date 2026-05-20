#axel m, malem and fernando
import pygame
import time
from spriteanimation_rectsfull import CharacterAnimator, AnimationState, load_zeldris_animations, load_rias_animations

pygame.init()

debug_mode = False

screen = pygame.display.set_mode((1280, 720))

running = True

clock = pygame.time.Clock()

zeldrisHealth = 100
riasHealth = 100

zeldrisBorder = False #the Border variables here are for detecting when the characters push against the edges of the screen
riasBorder = False #these are necessary for a scrolling background as the code needs to detect if both characters are on the edge so it can scroll

zeldrisX = 50
zeldrisY = 0

riasX = 300
riasY = 0

zeldrisVY = 0 #VY variables allows for gravity to function later in the code
riasVY = 0  #when the VY variable is used later, it becomes: VY minus gravity continuously
gravity = 0.3

pygame.key.set_repeat(500,1500)

repeats = 0 #This is a necessary variable for Zeldris fighting mechanic
#Zeldris doesn't have the typical Up-B and Down-X like Rias does
#Instead his attacks work by progressing the longer you hold down the X button in combination with right, down or left

SPRITE_SHEET = '2sprite.png'
SPRITE_SHEET2 = 'Fried.png'

# Player 1 animator (replaces the old char image — now animated from the sprite sheet)
zeldris = CharacterAnimator(SPRITE_SHEET, scale=2)
load_zeldris_animations(zeldris)
zeldris.facing_right = True

# Player 2 animator #Temporarily using a less compact method to test multiple players
rias = CharacterAnimator(SPRITE_SHEET2, scale=2) #This will get turned into a function later to possibly add more than 2 players
load_rias_animations(rias)
rias.facing_right = False

background = pygame.image.load("Background.png")
background = pygame.transform.scale(background, (int(background.get_width()*2.5), int(background.get_height()*3.22)))

zeldrisGround = False #Ground variables check if the character is touching the ground
riasGround = False

#By giving the background its own X and Y variables, we're able to make more creative maps that can scroll left to right or up and down

bgX_width = background.get_width()
bgY_height = background.get_height()

bg_X = 0
bg_Y = 0

platforms = [
    pygame.Rect(0,610,bgX_width,200), # floor collision
]

#Due to these having their own special effects on the game, they're seperate from other platforms
border_L = pygame.Rect(0,-50, 1, 800) #Rectangles are a bit larger than screen width to accomadate any accidental clipping during playtime
border_R = pygame.Rect(1280,-50, 1, 800)

zeldrisLose = False #Lose variables are used for when the character's hp reaches 0
riasLose = False #this allows the game to then load the WIN and LOSE animations and also finish the game

while running:
    screen.blit(background, (bg_X, bg_Y))

    # Get current frame sizes for collision rects
    p1_w = zeldris.current_image.get_width() if zeldris.current_image else 60
    p1_h = zeldris.current_image.get_height() if zeldris.current_image else 90
    p2_w = rias.current_image.get_width() if rias.current_image else 60
    p2_h = rias.current_image.get_height() if rias.current_image else 90

    zeldris.draw(screen, zeldrisX, zeldrisY)
    rias.draw(screen, riasX, riasY) # second player

    zeldris_rect = pygame.Rect(zeldrisX, zeldrisY, p1_w, p1_h)
    rias_rect = pygame.Rect(riasX, riasY, p2_w, p2_h)

    zeldrisVY = gravity + zeldrisVY
    riasVY = gravity + riasVY

    zeldrisY = zeldrisVY + zeldrisY
    riasY = riasVY + riasY

    for platform in platforms:
        if zeldris_rect.colliderect(platform):
            if zeldrisVY > 0: #checks if the character is coming from above (that's why it checks if VY is greater than 0)
                zeldrisVY = 0 #stops the continuous decrease
                zeldrisY = platform.top - p1_h
                zeldrisGround = True #pushes character to the top of the rectangle and marks the character as on the ground
            elif zeldrisVY < 0:  #checks if the character is coming from below (that's why it checks if VY is grealesster than 0)
                zeldrisVY = 0 #stops the continuous decrease
                zeldrisY = platform.bottom #makes it so the character can't push past the bottom
            if zeldrisX == platform.left:
                zeldrisX = platform.left - p1_w #uses platform's left and the width of the character because if it didn't, the character would get sent in the middle of the collision rectangle
            if zeldrisX == platform.right:
                zeldrisX = platform.right
        if rias_rect.colliderect(platform):
            if riasVY > 0:
                riasVY = 0
                riasY = platform.top - p2_h
                riasGround = True
            elif riasVY < 0:
                riasVY = 0
                riasY = platform.bottom
            if riasX == platform.left:
                riasX = platform.left - p2_w
            if riasX == platform.right:
                riasX = platform.right

#Different movement options (Using ijkl for zeldris and wasd for rias) with a jump and a special quick descent type move (when pressing down and off the ground) for fun

    keys = pygame.key.get_pressed()
    if keys[pygame.K_i] and (zeldrisGround == True): #checks if zeldris is grounded so he doesn't double jump/fly
        zeldrisVY = -8
    if keys[pygame.K_k]:
        if keys[pygame.K_o]: #makes it so when he's attacking using the o key, he doesn't move. this prevents the animations from getting confused and overloading the code
            zeldrisY = zeldrisY
        elif (zeldrisGround == False):
            zeldrisY = zeldrisY+1
    if keys[pygame.K_j]:
        if keys[pygame.K_o]:
            zeldrisX = zeldrisX
        else:
            zeldrisX = zeldrisX-10
            zeldris.facing_right = False
    if keys[pygame.K_l]:
        if keys[pygame.K_o]:
            zeldrisX = zeldrisX
        else:
            zeldrisX = zeldrisX+10
            zeldris.facing_right = True
    if keys[pygame.K_RSHIFT]:
        zeldrisX = zeldrisX
        zeldrisY = zeldrisY
    zeldrisGround = False #resets the value so it can be used again

    if keys[pygame.K_r] and (riasGround == True): #Rias has a jump key as she has Up and Aerial attacks
        riasVY = -8 #stops you from jumping when your on the floor and trying to use your up-B
    if keys[pygame.K_w]:
        riasY = riasY
    if keys[pygame.K_s]:
        if (riasGround == False):
            riasY = riasY+1
        else:
            riasY = riasY
    if keys[pygame.K_a]:
        riasX = riasX-10
        rias.facing_right = False
    if keys[pygame.K_d]:
        riasX = riasX+10
        rias.facing_right = True
    if keys[pygame.K_LSHIFT]:
        riasX = riasX
        riasY = riasY
    riasGround = False

    ZeldrisB = keys[pygame.K_u] #typically attacks are called by what they are on a controller. (Example: you use the b key on a console controller to active your UP-B)
    ZeldrisY = keys[pygame.K_o] #So I implemented that since it would be weird to call it UP-U
    ZeldrisX = keys[pygame.K_SEMICOLON]
    ZeldrisGuard = keys[pygame.K_RSHIFT]

    RiasB = keys[pygame.K_e]
    RiasY = keys[pygame.K_q]
    RiasX = keys[pygame.K_CAPSLOCK]
    RiasGuard = keys[pygame.K_LSHIFT]

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p: #makes it so you can quit the game using the p key
                running = False
            if event.key == pygame.K_o:
                print(str(repeats)) #for debugging to check what stage of Zeldris' attack the player is in
                repeats = repeats + 1 #adds one to repeat everytime the game checks if the O key is being held down
                if repeats > 2: #since Zeldris only has three stages to his attacks, repeat stops at 2
                    repeats = 2
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_o:
                repeats = 0 #once the O key is let go, the repeat value is reset for the next use
        if event.type == pygame.QUIT:
            running = False

    if zeldris_rect.colliderect(rias_rect): #checks for when zeldris is colliding with rias
        if ZeldrisB:
            riasHealth = riasHealth - 0.05 #subtracts health from rias depending on the move
        elif ZeldrisY:
            if ZeldrisY and (repeats == 0):
                riasHealth = riasHealth - 0.05
            elif ZeldrisY and (repeats == 1):
                riasHealth = riasHealth - 0.1
            elif ZeldrisY and (repeats == 2):
                riasHealth = riasHealth - 0.15
        elif ZeldrisX:
            riasHealth= riasHealth - 0.1


    if rias_rect.colliderect(zeldris_rect):
        if RiasB:
            if keys[pygame.K_w]:
                zeldrisHealth = zeldrisHealth - 0.1
            elif keys[pygame.K_s]:
                zeldrisHealth = zeldrisHealth - 0.1
            elif riasGround == False:
                zeldrisHealth = zeldrisHealth - 0.1
            else:
                zeldrisHealth = zeldrisHealth - 0.05
        elif RiasX:
            if keys[pygame.K_w]:
                zeldrisHealth = zeldrisHealth - 0.1
            else:
                zeldrisHealth = zeldrisHealth - 0.05
        elif RiasY:
            if keys[pygame.K_a]:
                zeldrisHealth = zeldrisHealth - 0.1
            elif keys[pygame.K_d]:
                zeldrisHealth = zeldrisHealth - 0.1
            elif keys[pygame.K_w]:
                zeldrisHealth = zeldrisHealth - 0.1
            elif keys[pygame.K_s]:
                zeldrisHealth = zeldrisHealth - 0.1
            elif riasGround == False:
                zeldrisHealth = zeldrisHealth - 0.1
            else:
                zeldrisHealth = zeldrisHealth - 0.05

    if keys[pygame.K_i]:
        zeldris.set_state(AnimationState.JUMP)
    elif ZeldrisY and keys[pygame.K_l]:
        if repeats == 0:
            zeldris.set_state(AnimationState.A1)
        elif repeats == 1:
            zeldris.set_state(AnimationState.A2)
        elif repeats == 2:
            zeldris.set_state(AnimationState.A3)
            if zeldris.finished(): #checks if the animation is finished and sets repeat to 0
                repeats = 0 #this is better than resetting it in the "for event in pygame.event.get():" section as it resets the repeat value when the animation is finished
                zeldris.set_state(AnimationState.IDLE)
    elif ZeldrisY and keys[pygame.K_k]:
        if repeats == 0:
            zeldris.set_state(AnimationState.B1)
        elif repeats == 1:
            zeldris.set_state(AnimationState.B2)
        elif repeats == 2:
            zeldris.set_state(AnimationState.B3)
            if zeldris.finished():
                repeats = 0
                zeldris.set_state(AnimationState.IDLE)
    elif ZeldrisY and keys[pygame.K_j]:
        if repeats == 0:
            zeldris.set_state(AnimationState.C1)
        elif repeats == 1:
            zeldris.set_state(AnimationState.C2)
        elif repeats == 2:
            zeldris.set_state(AnimationState.C3)
            if zeldris.finished():
                repeats = 0
                zeldris.set_state(AnimationState.IDLE)
    elif keys[pygame.K_l]:
        zeldris.set_state(AnimationState.WALK)
    elif keys[pygame.K_k]:
        zeldris.set_state(AnimationState.JUMP)
    elif keys[pygame.K_j]:
        zeldris.set_state(AnimationState.WALK)
    else:
        zeldris.set_state(AnimationState.IDLE)

    if keys[pygame.K_w] and RiasB:
        rias.set_state(AnimationState.UP_B)
    elif keys[pygame.K_w] and RiasX:
        rias.set_state(AnimationState.X_UP)
    elif keys[pygame.K_w] and RiasY:
        rias.set_state(AnimationState.UP_Y)
    elif keys[pygame.K_s]:
        rias.set_state(AnimationState.JUMP)
    elif keys[pygame.K_a]:
        rias.set_state(AnimationState.WALK)
    elif keys[pygame.K_d]:
        rias.set_state(AnimationState.WALK)
    else:
        rias.set_state(AnimationState.IDLE)

    font = pygame.font.SysFont(None, 36) #None so it uses the pygame default font and 36 is the size
    RiasText = font.render(f"Rias, Health: {riasHealth}", False, (255,255,255)) #using an f string as the code needs to print out variables
    ZeldrisText = font.render(f"Zeldris, Health: {zeldrisHealth}", False, (255,255,255)) #I wrote false after my f-string since I don't need antialiasing and then the next value is the color
    screen.blit(RiasText, (10, 10))
    screen.blit(ZeldrisText, (950, 10))

    if zeldrisHealth <= 0:
        zeldrisLose = True #the Lose variables are also used to print a message after it breaks out of the running loop
        zeldris.set_state(AnimationState.LOSE)
        rias.set_state(AnimationState.WIN)
        zeldrisX = zeldrisX
        zeldrisY = zeldrisY
        if zeldris.finished(): #checks if the animation is finished
            break

    if riasHealth <= 0:
        riasLose = True
        rias.set_state(AnimationState.LOSE)
        zeldris.set_state(AnimationState.WIN)
        riasX = riasX
        riasY = riasY
        if rias.finished():
            break

    zeldris.update()
    rias.update()

    if debug_mode:
        pygame.draw.rect(screen, (255 ,0, 0), zeldris_rect, 2)
        pygame.draw.rect(screen, (255 ,0, 0), rias_rect, 2) 
        for platform in platforms:
            pygame.draw.rect(screen, (255 ,0, 0), platform, 2)

    if zeldris_rect.colliderect(border_L):
        zeldrisBorder = True
        if riasBorder and zeldrisBorder:
            if bg_X >= ((bgX_width - bgX_width)): #(bgX_width - bgX_width) is a constant used to make the comparison work. The reason "0" isn't used is because this can provide a more specific value for the comparison
                bg_X = -10 #We set bg_X to -10 as that's how much the player moves. Any less and the background would get a bit glitchy.
            bg_X = bg_X + 10 #adds to the bg_X value to move left
        zeldrisX = border_L.right

    if zeldris_rect.colliderect(border_R):
        zeldrisBorder = True
        if riasBorder and zeldrisBorder:
            if bg_X <= ((-bgX_width + 1280)):
                bg_X = ((-bgX_width + 1280) + 10)
            bg_X = bg_X - 10
        zeldrisX = border_R.left - p1_w

    if rias_rect.colliderect(border_L):
        riasBorder = True
        if riasBorder and zeldrisBorder:
            if bg_X >= ((bgX_width - bgX_width)): #(bgX_width - bgX_width) is a constant used to make the comparison work. The reason "0" isn't used is because this can provide a more specific value for the comparison
                bg_X = -10 #
            bg_X = bg_X
        riasX = border_L.right

    if rias_rect.colliderect(border_R):
        riasBorder = True
        if riasBorder and zeldrisBorder:
            if bg_X <= ((-bgX_width + 1280)):
                bg_X = ((-bgX_width + 1280) + 10)
            bg_X = bg_X - 10
        riasX = border_R.left - p2_w

    clock.tick(25)

    pygame.display.flip()

if riasLose:
    print("Zeldris Wins!")

if zeldrisLose:
    print("Rias Wins!")

pygame.quit()
