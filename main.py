import pygame
import _tempFunct

pygame.init()
pygame.display.set_caption("wireWorld")
clock = pygame.time.Clock()

windowSize = [518, 518]  # windows size
screen = pygame.display.set_mode(windowSize)  # display
myFont = pygame.font.SysFont("Times New Roman", 18)  # font

width = 8  # size of the grid in px
height = 8
margin = 1  # margin between the grid

hSize = 48  # amount of grids
wSize = 48

# create basic colors
c_red = (255, 0, 0)
c_blue = (0, 0, 255)
c_green = (0, 255, 0)
c_white = (255, 255, 255)
c_black = (0, 0, 0)
c_yellow = (255, 240, 2)

grid = []  # create blank grid
elements = 2  # amount of grid types

mouseState = "nothing"  # checks what action was performed by mouse
LEFT = 1  # lmb
RIGHT = 3  # rmb
leftHold = False
rightHold = False
sparkTimer = 0  # time after which you will be able to spark the wire, after building it

# two dimensional array of the grid and grid data, values of the grid define type of the particle
for column in range(wSize+2):
    grid.append([])
    for row in range(hSize+2):
        grid[column].append([])
        grid[column][row] = 0  # initialise tiles with void at them

# data grid
partAmount = 5  # amount of created particle types
partDataAmount = 5  # amount of particle stats
partData = [[0 for x in range(partAmount)] for y in range(partDataAmount)]   # create blank particle database

partCheck = [[0 for x in range(wSize+2)] for y in range(hSize+2)]   # create blank change check array

# two dimensional array of the particle database
# 0 void###
arrType = 0  # changes particle type so it's faster to input database
partData[arrType][0] = "Void"  # name
partData[arrType][1] = c_white  # sprite/color

# 1 wire ###
arrType = 1
partData[arrType][0] = "Wire"
partData[arrType][1] = c_red

# 2 head ###
arrType = 2
partData[arrType][0] = "Head"
partData[arrType][1] = c_green

# 3 tail ###
arrType = 3
partData[arrType][0] = "Tail"
partData[arrType][1] = c_blue

changeCounter = 0  # amount of changes around tile
timer = 0  # grid loop timer, to allow multiple checks after state change
stepTime = 1  # time between state changes

while True:  # initial loop ________________________________________________________________________________
    screen.fill(c_black)

    # define step stuff
    # mouse position
    pos = pygame.mouse.get_pos()
    mouse_x = pos[0]  # x position of the mouse
    mouse_y = pos[1]  # y position of the mouse

    xPos = int(mouse_x / (height + margin))  # read x cell
    yPos = int(mouse_y / (width + margin))  # read y cell

    # create grid loops
    timer += 1  # timer for grid loops
    near = 0  # amount of nearby sparks

    if leftHold is False:
        sparkTimer -= 1  # decrement time required between wire placement and sparking

    if timer > stepTime:
        timer = 0
        for column in range(1, wSize+1):
            for row in range(1, hSize+1):
                grid[column][row] = partCheck[column][row]  # change current type to saved one

    if timer > stepTime-1:
        for column in range(1, wSize+1):
            for row in range(1, hSize+1):
                curTile = grid[column][row]  # read type of the current tile
                
                # initial type > output type
                
                # tail > wire
                if grid[column][row] == 3:
                    # grid[column][row] = 1
                    partCheck[column][row] = 1

                # head > tail
                if grid[column][row] == 2:
                    # grid[column][row] = 3
                    partCheck[column][row] = 3

                # wire > head
                if grid[column][row] == 1:
                    near = 0  # neighbors
                    if grid[column - 1][row] == 2:
                        near += 1
                    if grid[column - 1][row - 1] == 2:
                        near += 1
                    if grid[column + 1][row] == 2:
                        near += 1
                    if grid[column + 1][row + 1] == 2:
                        near += 1
                    if grid[column - 1][row + 1] == 2:
                        near += 1
                    if grid[column + 1][row - 1] == 2:
                        near += 1
                    if grid[column][row + 1] == 2:
                        near += 1
                    if grid[column][row - 1] == 2:
                        near += 1

                    if near == 1 or near == 2:
                        # grid[column][row] = 2
                        partCheck[column][row] = 2

                # drawing and tile change
    for column in range(1, wSize + 1):
        for row in range(1, hSize + 1):
            curTile = grid[column][row]  # read type of the current tile
            color = partData[curTile][1]

            # draw tile rectangle
            pygame.draw.rect(screen, color, (margin + (width + margin) * column, margin + (height + margin) * row, width, height))

    # _tempFunct.draw_text(screen, myFont, 400, 400, str(sparkTimer), c_red)  # used for debug

    # check if something happened///////////////
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:  # checks mouse left click
            mouseState = "clickLeft"
            leftHold = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == LEFT:  # checks mouse left up
            mouseState = "upLeft"
            leftHold = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:  # checks mouse right click
            mouseState = "clickRight"
            rightHold = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == RIGHT:  # checks mouse right up
            mouseState = "upRight"
            rightHold = False
        else:
            mouseState = "nothing"

        if leftHold:
            if grid[xPos][yPos] == 0:
                grid[xPos][yPos] = 1  # grid type change to wire
                partCheck[xPos][yPos] = 1
                sparkTimer = 3
        if leftHold and sparkTimer <= 0:
            if grid[xPos][yPos] == 1:
                grid[xPos][yPos] = 2  # grid type change to head
                partCheck[xPos][yPos] = 2

        if rightHold:
            if grid[xPos][yPos] == 1 or grid[xPos][yPos] == 2 or grid[xPos][yPos] == 3:
                grid[xPos][yPos] = 0  # grid type change to wire
                partCheck[xPos][yPos] = 0

    # pygame clock
    clock.tick(60)
    pygame.display.flip()
