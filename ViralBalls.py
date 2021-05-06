import pygame
from time import sleep
import math
import numpy as np

def Grid_init() :
    
    for i in range(0, screen_height, cell_size+1):
        for j in range(0, screen_width, cell_size+1) :
            pygame.draw.rect(screen, colors[0], pygame.Rect(j, i, cell_size, cell_size))
            
def which_cell(left, top) :
    if (left == 0 and top == 0) or (left == 360 and top == 0) or (left == 360 and top == 450) or (left == 0 and top == 450) :
        return 'corner'
    
    elif (left == 0 and top in range (1, 450)) or (left == 360 and top in range (1, 450)) or (left in range(1, 360) and top == 450) or (left in range(1, 360) and top == 0) :
        return 'edge'
    
    else:
        return 'inner'


def empty_cell(left, top) :
    pygame.draw.rect(screen, colors[0], pygame.Rect(left, top, cell_size, cell_size))

def draw_circle(left, top, color) :
    
    cell_col, cell_row =  left//cell_size, top//cell_size
    num_circles = Grid_Circles[cell_row][cell_col][0]
    empty_cell(left, top)
    Grid_Circles[cell_row][cell_col][0] = 0
    Grid_Circles[cell_row][cell_col][1] = -1
    #selected cell having zero circle 
    if num_circles == 0 :
        draw_one_circle(left, top, color)
    
    elif num_circles == 1 :
        
        # if it is a corner case, we need to split it diagonally
        if which_cell(left, top) == 'corner' :
            if left == 0 :
                new_left = left + cell_size + 1
            else : new_left = left - cell_size - 1

            if top == 0 :
                new_top = top + cell_size + 1
            else : new_top = top - cell_size - 1

            draw_circle(new_left, top, color )
            draw_circle(left, new_top, color)

        else :
            draw_two_circle(left, top, color)

    elif num_circles == 2 :
        if which_cell(left, top) == 'edge' :
            if left == 0 :
                draw_circle(left + cell_size + 1, top, color)
                draw_circle(left, top + cell_size + 1, color)
                draw_circle(left, top - cell_size - 1, color)

            elif left == 360 : 
                draw_circle(left - cell_size - 1, top, color)
                draw_circle(left, top + cell_size + 1, color)
                draw_circle(left, top - cell_size - 1, color)
            

            elif top == 0 :
                draw_circle(left, top + cell_size + 1, color)
                draw_circle(left + cell_size + 1, top, color)
                draw_circle(left - cell_size - 1, top, color)
            
            elif top == 450 :
                draw_circle(left, top - cell_size - 1, color)
                draw_circle(left + cell_size + 1, top, color)
                draw_circle(left - cell_size - 1, top, color)
            
        else:
            draw_three_circle(left, top, color)

    elif num_circles == 3 :
        draw_circle(left, top + cell_size + 1, color)
        draw_circle(left, top - cell_size - 1, color)
        draw_circle(left + cell_size + 1, top, color)
        draw_circle(left - cell_size - 1, top, color)


def draw_one_circle(left, top, color) :
    
    empty_cell(left, top)
    cell_col, cell_row =  left//cell_size, top//cell_size

    pygame.draw.rect(screen, colors[0], pygame.Rect(left, top, cell_size, cell_size))
    pygame.draw.circle(screen, colors[color], (left+14, top+14), ball_radius)
    
    # updating the number of circles and color for the current cell
    Grid_Circles[cell_row][cell_col][0] = 1
    Grid_Circles[cell_row][cell_col][1] = color

def draw_two_circle(left, top, color) :
    
    empty_cell(left, top)
    cell_col, cell_row =  left//cell_size, top//cell_size

    pygame.draw.circle(screen, colors[color], (left+ball_radius+1, top+cell_size/2), ball_radius)
    pygame.draw.circle(screen, colors[color], (left+cell_size-ball_radius-1, top+cell_size/2), ball_radius)
    
    Grid_Circles[cell_row][cell_col][0] = 2
    Grid_Circles[cell_row][cell_col][1] = color

def draw_three_circle(left, top, color) :
    
    empty_cell(left, top)
    cell_col, cell_row =  left//cell_size, top//cell_size

    pygame.draw.circle(screen, colors[color], (left+ball_radius+1, top+cell_size -ball_radius - 1), ball_radius)
    pygame.draw.circle(screen, colors[color], (left+cell_size-ball_radius-1, top+cell_size-ball_radius-1), ball_radius)
    pygame.draw.circle(screen, colors[color], (left+cell_size/2, top+ball_radius+1), ball_radius)
    
    Grid_Circles[cell_row][cell_col][0] = 3
    Grid_Circles[cell_row][cell_col][1] = color

def defeat() :
    init_color = -1
    for i in range(len(Grid_Circles)) :
        for j in range (len(Grid_Circles[0])) :
            if Grid_Circles[i][j][1] != -1 and init_color == -1 :
                init_color = Grid_Circles[i][j][1] 
            
            elif Grid_Circles[i][j][1] != -1 and  init_color !=  Grid_Circles[i][j][1] : 
                return False
    
    return True


#defining colors to use in the game
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
colors = [black, red, green, blue, white]

#initializing parameters for the game screen 
pygame.init()
screen_height, screen_width = 480, 390
screen = pygame.display.set_mode((screen_width, screen_height))
screen.fill(white)
pygame.mouse.set_cursor(pygame.cursors.tri_left)
cell_size  = 29
ball_radius = 8

Grid_Circles = [[[0, -1]]*(screen_width//cell_size) for _ in range(screen_height//cell_size)]
Grid_Circles = np.array(Grid_Circles)
Grid_init()

#enter Player names
Pl1 = input('Enter Player 1 name: ')
Pl2 = input('Enter Player 2 name: ')
cur_player = Pl1
First_run = True
done = False

#start with Player 1
pygame.display.set_caption(cur_player + "'s turn..")

Player1 = True
Player2 = False
color = 2

#from here the game starts untill we close the game window
while not done:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    done = True

            elif event.type == pygame.MOUSEBUTTONUP :
                x, y = pygame.mouse.get_pos()
                
                horizontal_borders_between =  math.ceil(x//cell_size)
                vertical_borders_between  = math.ceil(y//cell_size)

                left = math.floor((x - horizontal_borders_between) // cell_size) * cell_size + (x - horizontal_borders_between)//cell_size
                top = math.floor((y - vertical_borders_between) // cell_size) * cell_size + (y - vertical_borders_between)//cell_size
                width = left + cell_size 
                height = top + cell_size 

                cell_col, cell_row =  left//cell_size, top//cell_size

                if Grid_Circles[cell_row][cell_col][0] == 0 :
                    
                    draw_one_circle(left, top, color)
                    Player1 = not Player1
                    Player2 = not Player2
                    if cur_player == Pl1  : cur_player = Pl2
                    else : cur_player = Pl1
                    if color==2 : color = 3
                    else: color = 2


                elif Grid_Circles[cell_row][cell_col][0] == 1 and color == Grid_Circles[cell_row][cell_col][1] :
                    
                    draw_circle(left, top, color)    
                    Player1 = not Player1
                    Player2 = not Player2
                    if cur_player == Pl1  : cur_player = Pl2
                    else : cur_player = Pl1
                    if color==2 : color = 3
                    else: color = 2


                elif Grid_Circles[cell_row][cell_col][0] == 2 and color == Grid_Circles[cell_row][cell_col][1] :
                    
                    draw_circle(left, top, color)
                    Player1 = not Player1
                    Player2 = not Player2
                    if cur_player == Pl1  : cur_player = Pl2
                    else : cur_player = Pl1
                    if color==2 : color = 3
                    else: color = 2

                elif Grid_Circles[cell_row][cell_col][0] == 3 and color == Grid_Circles[cell_row][cell_col][1] :
                    
                    draw_circle(left, top, color)
                    Player1 = not Player1
                    Player2 = not Player2
                    if cur_player == Pl1  : cur_player = Pl2
                    else : cur_player = Pl1
                    
                    if color==2 : color = 3
                    else: color = 2
            
                if defeat() and First_run == False:
                    if cur_player == Pl1  : cur_player = Pl2
                    else : cur_player = Pl1
                    
                    font = pygame.font.Font('freesansbold.ttf', 32)
                    text = font.render(f'{cur_player} WON THE GAME', True, green, blue)
                    textRect = text.get_rect()
                    textRect.center = (screen_width // 2, screen_height // 2)
                    screen.fill(white)
                    screen.blit(text, textRect)
                    pygame.display.flip()
                    sleep(10)

                    done = True

                First_run = False

            pygame.display.set_caption(cur_player + "'s turn..")    
                
    
    pygame.display.flip()
