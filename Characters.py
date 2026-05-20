import pygame
import spriteanimation as anims

#Character.py would use the IDLE as a character selection screen

#Values would be saved in lists so they can be called from in the Main.py

getLoop = True

charList = [ # list of characters to choose from
    Zeldras,
    Rias
]

charsPlay = [ # characters that will be played in the session

]

charX = [ #X values

]

charY = [ #Y values

]

charVY = [ # VY values

]

charBorder = [ # Border values

]

charGround = [ # Ground values

]

charNumber = 0 # number of characters stored in an integer value

#charNumber would be stuck on the end of the character's name in charsPlay

#this makes it easy to call from duplicates if you want to call them by name

input = pygame.key.get_pressed()

def getChar:
    while getLoop: # starts a loop to get a response
        print("Characters: ")
        for char in charList: # prints chars from list
            print(char)
        charChoice = input("Choose your character: ")
            if charChoice in charlist: # if the character is a character from the list, it'll append all the associate values
                charsPlay.append(charChoice)
                charX.append(x+str(charNumber))
                charY.append(y+str(charNumber))
                charVY.append(vy+str(charNumber))
                charBorder.append(border+str(charNumber))
                charGround.append(ground+str(charNumber))
            else:
                print("Please enter a valid character")
        charNumber + 1 # add one to charNumber so it can preserve uniqueness
        getContinue = input("Would you like to add another character? (y/n) ")
            if getContinue = "y":
                print("Please add next character")
            elif getContinue = "n":
                return #returns values
            else:
                print("Please enter a valid response")
