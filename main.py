import pygame

pygame.init()
pygame.display.set_caption("wireWorld")
clock = pygame.time.Clock()

windowSize = [518, 518]  # windows size
screen = pygame.display.set_mode(windowSize)  # set display
myFont = pygame.font.SysFont("Times New Roman", 18)  # font

width = 8  # size of the cell in px
height = width
margin = 1  # margin between the cells

hSize = 48  # amount of cells
wSize = 48

# create basic colors
c_red = (255, 0, 0)
c_blue = (0, 0, 255)
c_green = (0, 255, 0)
c_white = (255, 255, 255)
c_black = (0, 0, 0)
c_yellow = (255, 240, 2)

LEFT = 1  # lmb
RIGHT = 3  # rmb
leftHold = False
rightHold = False
sparkTimer = 0  # time after which you will be able to spark the wire, after building it

# two dimensional array of the grid and grid data, values of the grid define type of the particle
grid = []  # create blank grid
for column in range(wSize+2):
    grid.append([])
    for row in range(hSize+2):
        grid[column].append([])
        grid[column][row] = 0  # initialise tiles with void at them

# data grid
partAmount = 5  # amount of created particle types
partDataAmount = 2  # amount of particle stats
partCheck = [[0 for x in range(wSize+2)] for y in range(hSize+2)]   # create blank change check array
partData = []  # create blank particle database
for x in range(partAmount):
    partData.append([])
    for y in range(partDataAmount):
        partData[x].append([])

# two dimensional array of the particle database
# 0 void ###
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

# 4 temporary head ###
arrType = 4
partData[arrType][0] = "TempHead"
partData[arrType][1] = c_green

changeCounter = 0
timer = 0
stepTime = 1


# read position of the cell from mouse position 0 = x, 1 = y
def mouse_pos(axis):
    get_pos = pygame.mouse.get_pos()
    position = get_pos[axis]  # position of the mouse

    return int(position / (width + margin))  # read x cell


# update the gird
def update_cells():
    for y in range(1, wSize + 1):
        for x in range(1, hSize + 1):
            grid[y][x] = partCheck[y][x]


# change type of the cells during step
def change_types():
    for y in range(1, wSize + 1):
        for x in range(1, hSize + 1):
            # tail -> wire
            if grid[y][x] == 3:
                partCheck[y][x] = 1

            # head -> tail
            if grid[y][x] == 2:
                partCheck[y][x] = 3

            # wire -> head
            if grid[y][x] == 1:
                check_neighbors(x, y)


# check neighboring cells and their type
def check_neighbors(x, y):
    near = 0  # amount of neighbors

    for i in (-1, 0, 1):
        for n in (-1, 0, 1):
            if grid[y + i][x + n] == 2:
                near += 1

    if near == 1 or near == 2:
        partCheck[y][x] = 2


# draw the grid
def draw_grid():
    for x in range(1, wSize + 1):
        for y in range(1, hSize + 1):
            cur_tile = grid[x][y]  # read type of the current tile
            color = partData[cur_tile][1]

            # draw tile rectangle
            cell_position = (margin + (width + margin) * x, margin + (height + margin) * y, width, height)
            pygame.draw.rect(screen, color, cell_position)


def click_check(button_left, button_right, spark_timer):
    if button_left:
        if grid[xPos][yPos] == 0:
            grid[xPos][yPos] = 1  # grid type change to wire
            partCheck[xPos][yPos] = 1
            global sparkTimer
            sparkTimer = 3
    if button_left and spark_timer <= 0:
        if grid[xPos][yPos] == 1:
            grid[xPos][yPos] = 2  # grid type change to head
            partCheck[xPos][yPos] = 2

    if button_right:
        if grid[xPos][yPos] == 1 or grid[xPos][yPos] == 2 or grid[xPos][yPos] == 3:
            grid[xPos][yPos] = 0  # grid type change to wire
            partCheck[xPos][yPos] = 0


while True:  # initial loop ________________________________________________________________________________
    screen.fill(c_black)

    # mouse position
    xPos = mouse_pos(0)
    yPos = mouse_pos(1)

    # create grid loops
    timer += 1  # timer for grid loops

    if leftHold is False:
        sparkTimer -= 1  # decrement time required between wire placement and sparking

    if timer > stepTime:
        timer = 0
        update_cells()

    if timer > stepTime-1:
        change_types()

    # cell drawing and visual change
    draw_grid()

    # check inputs
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:  # checks mouse left click
            leftHold = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == LEFT:  # checks mouse left up
            leftHold = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:  # checks mouse right click
            rightHold = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == RIGHT:  # checks mouse right up
            rightHold = False

        click_check(leftHold, rightHold, sparkTimer)

    # pygame clock and flush
    clock.tick(60)
    pygame.display.flip()
