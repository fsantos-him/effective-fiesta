# Invincibility

## Brief Description

This 2D fighting game takes place in an arena with you and one other person. You will be playing until the first person gets knocked out (Health reaches 0). There will be different styles of combat that each person can use.

## Fighting Styles

Zeldris and Rias have different fighting styles, making it so they have different movesets.

For example, holding down X alongside either the Down, Left or Right keys will allow Zeldris to sort through the phases of his attacks

However, Rias uses the Movement+Attack Key (example:like an UP-B in Super Smash Bros.) formula to fight 

## Future Content

### Ultimates

Each fighting style has its own ultimate. These ultimates are charged up by receiving or dealing blows. Receiving blows charges up the ultimates faster than dealing blows. Your progress towards an ultimate is shown on the screen in a bar.

### Passives

These are skills than can be used throughout the fight without any player input

## How to Play

### Zeldris Controls:
I = Jump
K = Down
J = Left
L = Right 
O = X
; = Y 
U = Special
Right Shift = Guard

### Rias Controls:
R = Jump
W = Up
S = Down
A = Left
D = Right 
Q = X 
CapsLock = Y 
E = Special
Left Shift = Guard


## Features

Collision Tracking
Health Tracking 
Scrolling Background 
Animated Sprites 
Unique Fighting Styles


## Installation / How to Run

Download Python IDLE
Download game files from Github
Open Python IDLE
CLick on File (top left corner) and click Open
Select the py file from the game files and click enter
In the new window, press F5 to run the game
The Team

-Axel- Head Coder

> I plan to add functionality to this game by implementing movement, attacks, and other special features. I will also help with the visual appeal and general presentation of the game

-Malem- Chief Coder

-Fernando- Researcher/Coder

> I will plan on adding a good addition of coding to help the Head Coder and will also research the information we need for the game

### 4/27
One thing we added was having the background move as the character moves and this was also the challenge we ran into.

### 4/28
Removed Space Key as the Up Key works fine and makes more sense for our future endeavors (adding multiplayer)
Moved the floor's collision rectangle to the platform list and implemented the code for the platforms and debug mode into the game 
Changed the size of the borders on each side of the screen to accommodate for clipping issues 
Added comments to explain some of our choices (Using generic names for the background and character as well as why we only use one image for each rather than a function which takes images from a folder)
Changed the speed at which the background moves

# TIMELINE

## Accomplished
Fernando - Finding a character and background and Select character screen. Got the sprite for the character and took screenshots of each animation in case ENUM goes haywire but also to test it. Reviewing the code and seeing if a different route needs to be changed.

Axel - Implemented the screen and character to our code. Also figuring out how to have our background move as we walk to make our game a bit more interesting. Also organized the code so it wont be sloppy. Axel is working on having our character not glitch out of our screen when moving a certain way.

Malem - Found another character to use and searched up on how to easily get out sprite characters to work. Found ENUM which could be incredibly useful and is working on how to implement it in the code. Is also keeping a watch on the code and gathering some information that could be used.

## Future Milestones

First period after presentation is working on sprite animation to have our character look alive and not have it js be an image

2nd period after that is having it complete some moves we gathered to add some unique effects to our game 

3rd Period after that is to add another character which should be relatively easy and try to include the sprite animation

4th period is to update our trackers for score, health, and ultimate charge up. 

5th period is where we will work on the collision between the characters so it truly becomes a fighting game and start on making the starting screen and a select your character screen

6-7 period is to work on any bugs that come along the process and polishing up on some of the code so the game can run fluently.

# Python Programming Final

### Axel's contributions: 

Axel added the scrolling function for the background, the text at the top for health, a way of tracking if the current animation is finished, and the method of tracking Zeldris' progress through the phases of his attack. Changed some of Fernando's code to use elifs and ifs so that the game would run smoother. Alongside Fernando, added comments and cleaned up code. 

### Fernando's contributions: 

Fernando managed the rectangles for the animations, adding new animations, variables for attacking and guarding, the keys for movement, and the keybinds, collisions and damage numbers for attacking. Also, helped with making the comments understandable

### How the game should work + Current state of the game

You can move both characters easily and fight each other. You can also decide to move the background by getting both characters to push on a border at the same time. Once someone falls below 0 hp, the character will stay in their WIN or LOSE animation. You win by lowering the other person's hp to 0 or below.
Functionality wise, the code for guarding and ultimates as well as the code for loading the animations for Rias and Zeldris' specials and other parts of their movesets needs to be implemented. 
Visually, the sprites are sometimes loaded in weird (for example when Zeldris attacks with his big purple sword) causing the image to load in weird
Right now, it's about 60% done, as the code for these functions is easy but will take more time. 

For guarding: 
Using the repeat function, a new variable for tracking how many times the guard key is held down will be implemented. 
When it reaches 3, immobilize the player for a set period of time and make it so they take a big amount of damage

For ultimates: 
Works the same way as usual attacks but spawns in a projectile using blit. 
When that projectile reaches the outside of one of screen borders, delete the projectile

### Bugs and Issues

Even after a character's health reaches 0, both characters can still attack and the game doesn't close. 
Sometimes Zeldris can glitch through the floor if you jump and press down at the right time
When a character's health reaches 0, if you try to attack as Zeldris, he disappears 
Sprites can be loaded in weird at times.

### What would we have done with more time

We would've fixed the sprite issues, 
Implemented guarding, ultimates, passives and the code for loading the missing moves from each character's moveset,
Added a way of choosing how many characters you wanted, what characters you wanted, what background you wanted, and allowed each player to select what passive ability they wanted through IDLE, 
Added unique UI, 
And added more characters and backgrounds.

