from __future__ import division
import pygame

track_size = [50, 50]#m

FLOOR_WIDTH_PXL = 300 #have to be more than max values of box
FLOOR_HEIGHT_PXL = 400
SCREEN_WIDTH_PXL = 1350
SCREEN_HIGHT_PXL = 680
SOLUTION_WIDTH_PXL = 400

FPS = 100

BLACK = (  0,   0,   0)    
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
GREY  = (200, 200, 200)



DRAW_SCALE = (min(SCREEN_HIGHT_PXL, SCREEN_WIDTH_PXL)/ (max(track_size)))


def Draw_Walls(DISPLAYSURF, walls):
    walls = walls * DRAW_SCALE
    for i in walls:
        pygame.draw.line(DISPLAYSURF, BLACK, i[0], i[1], 4)
    
    pygame.draw.line(DISPLAYSURF, RED, [5 * DRAW_SCALE, 0 * DRAW_SCALE], [5 * DRAW_SCALE, 5 * DRAW_SCALE], 4)
    pygame.draw.line(DISPLAYSURF, GREEN, [0 * DRAW_SCALE, 5 * DRAW_SCALE], [5 * DRAW_SCALE, 5 * DRAW_SCALE], 4)
    #pygame.draw.line(DISPLAYSURF, BLACK, [1 * DRAW_SCALE, 5 * DRAW_SCALE], [45 * DRAW_SCALE, 5 * DRAW_SCALE], 4)
    #pygame.draw.line(DISPLAYSURF, BLACK, [1 * DRAW_SCALE, 1 * DRAW_SCALE], [50 * DRAW_SCALE, 50 * DRAW_SCALE], 4)

def Floor_Drawing(DISPLAYSURF, solution_Num):
    global solution_Border
    global solution_Border_up_down
    floor_Border = 6
    line_Width = 4
    solution_Border = (SOLUTION_WIDTH_PXL - FLOOR_WIDTH_PXL)/2
    solution_Border_up_down = (SCREEN_HIGHT_PXL - SOLUTION_WIDTH_PXL)/2
    bottom_Left_Dot = SOLUTION_WIDTH_PXL*solution_Num+solution_Border
    pygame.draw.rect(DISPLAYSURF, BLACK, (bottom_Left_Dot-floor_Border,solution_Border_up_down-floor_Border,FLOOR_WIDTH_PXL+2*floor_Border,FLOOR_HEIGHT_PXL+2*floor_Border))
    pygame.draw.rect(DISPLAYSURF, WHITE, (bottom_Left_Dot,solution_Border,FLOOR_WIDTH_PXL,SCREEN_HIGHT_PXL-2*solution_Border))
    pygame.draw.line(DISPLAYSURF, BLUE, (SOLUTION_WIDTH_PXL*(solution_Num+1),0),(SOLUTION_WIDTH_PXL*(solution_Num+1),SCREEN_HIGHT_PXL),line_Width)

def Box_Drawing (DISPLAYSURF,solution_num,box_num, x,y,a,b,color,angle, out_of_box = False):
    box_border = 1
    if out_of_box:
        color = RED
    pygame.draw.rect(DISPLAYSURF, BLACK, (solution_num * SOLUTION_WIDTH_PXL + solution_Border + x, solution_Border_up_down + FLOOR_HEIGHT_PXL - y, a, -b))
    pygame.draw.rect(DISPLAYSURF, color,(solution_num * SOLUTION_WIDTH_PXL + solution_Border + x + box_border,solution_Border_up_down + FLOOR_HEIGHT_PXL - (y+box_border),a-2*box_border,-(b-2*box_border)))
    myfont = pygame.font.SysFont('Comic Sans', 20)
    textsurface = myfont.render(str(box_num), False, BLACK)
    DISPLAYSURF.blit(textsurface,(solution_num * SOLUTION_WIDTH_PXL + solution_Border + x+box_border,solution_Border_up_down + FLOOR_HEIGHT_PXL - (y+box_border) -(b-2*box_border)))
    
def Graph(DISPLAYSURF, costs):
    if len(costs) < 5:
        return
    border = 15
    line_width = 2
    steps = int(len(costs) / 10) + 1
    
    pygame.draw.line(DISPLAYSURF, BLACK, (2 * SOLUTION_WIDTH_PXL + border, border), (2 * SOLUTION_WIDTH_PXL + border, SCREEN_HIGHT_PXL- border), line_width)
    pygame.draw.line(DISPLAYSURF, BLACK, (2 * SOLUTION_WIDTH_PXL + border, SCREEN_HIGHT_PXL- border), (SCREEN_WIDTH_PXL - border, SCREEN_HIGHT_PXL- border), line_width)
    
    minimal = min(costs)
    maximal = max(costs)
    previous_cost = costs[0] - minimal
    scale_X = (SCREEN_WIDTH_PXL - 2 * SOLUTION_WIDTH_PXL - 2 * border) / len(costs)
    scale_Y = (SCREEN_HIGHT_PXL - 2 * border) / (maximal - minimal + 0.001 )
    i = 0
    for cost in costs:
        cost = cost - minimal
        pygame.draw.line(DISPLAYSURF, RED, (SOLUTION_WIDTH_PXL * 2 + border + i * scale_X, SCREEN_HIGHT_PXL - border - previous_cost * scale_Y), (SOLUTION_WIDTH_PXL * 2 + border + (i+1) * scale_X, SCREEN_HIGHT_PXL - border - cost * scale_Y), line_width)
        i = i + 1
        if not(i % steps):
            myfont = pygame.font.SysFont('Comic Sans', 15)
            textsurface = myfont.render(str(i), False, BLACK)
            DISPLAYSURF.blit(textsurface,(SOLUTION_WIDTH_PXL * 2 + border + i * scale_X, SCREEN_HIGHT_PXL - border + 3))
            
            textsurface = myfont.render((str(round(cost+minimal,3) * 100)) + "%", False, BLACK)
            DISPLAYSURF.blit(textsurface,(SOLUTION_WIDTH_PXL * 2 + border  + i * scale_X + 2, SCREEN_HIGHT_PXL - border - cost * scale_Y + 3))
            
            
        previous_cost = cost
        
    myfont = pygame.font.SysFont('Comic Sans', 40)
    textsurface = myfont.render(str(round(maximal,3) * 100) + "%", False, BLACK)
    DISPLAYSURF.blit(textsurface,(SCREEN_WIDTH_PXL - 150, SCREEN_HIGHT_PXL - 50))
        
        
        
    
        