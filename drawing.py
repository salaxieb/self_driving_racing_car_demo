from __future__ import division
import pygame
from numpy import *
random.seed(1234567890)

track_size = [60, 50]#m

FLOOR_WIDTH_PXL = 300 #have to be more than max values of box
FLOOR_HEIGHT_PXL = 400
SCREEN_WIDTH_PXL = 1200
SCREEN_HEIGHT_PXL = 500

FPS = 50

BLACK = (  0,   0,   0)    
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
GREY  = (200, 200, 200)



DRAW_SCALE = (min(SCREEN_WIDTH_PXL/track_size[0], SCREEN_HEIGHT_PXL/track_size[1]))
MAP_WIDTH = track_size[0] * DRAW_SCALE


def Draw_Map(DISPLAYSURF, map, cycle_time):
#     print (type(cycle_time))
    if type(cycle_time) == int:
        cycle_time = str(round(cycle_time,1))
    walls = array(map.walls) * DRAW_SCALE
    for wall in walls:
        pygame.draw.line(DISPLAYSURF, BLACK, wall[0], wall[1], 4)    
    pygame.draw.line(DISPLAYSURF, GREEN, array(map.start_line[0])*DRAW_SCALE, array(map.start_line[1])*DRAW_SCALE, 4)
    pygame.draw.line(DISPLAYSURF, RED, array(map.finish_line[0])*DRAW_SCALE, array(map.finish_line[1])*DRAW_SCALE, 4)
    #pygame.draw.line(DISPLAYSURF, BLACK, [1 * DRAW_SCALE, 5 * DRAW_SCALE], [45 * DRAW_SCALE, 5 * DRAW_SCALE], 4)
    #pygame.draw.line(DISPLAYSURF, BLACK, [1 * DRAW_SCALE, 1 * DRAW_SCALE], [50 * DRAW_SCALE, 50 * DRAW_SCALE], 4)
    myfont = pygame.font.SysFont('Comic Sans', 15)
    textsurface = myfont.render(cycle_time, False, BLACK)
    DISPLAYSURF.blit(textsurface,(2,2))

def Graph(DISPLAYSURF, scores):
    if len(scores) < 3:
        return
    border = 15
    line_width = 2
    steps = int(len(scores) / 20) + 1
    
    pygame.draw.line(DISPLAYSURF, BLACK, (MAP_WIDTH + border, border), (MAP_WIDTH + border, SCREEN_HEIGHT_PXL- border), line_width)
    pygame.draw.line(DISPLAYSURF, BLACK, (MAP_WIDTH + border, SCREEN_HEIGHT_PXL- border), (SCREEN_WIDTH_PXL - border, SCREEN_HEIGHT_PXL- border), line_width)
    
    minimal = 0#min(scores)
    maximal = max(scores)
    previous_cost = scores[0] - minimal
    scale_X = (SCREEN_WIDTH_PXL - MAP_WIDTH - 2 * border) / len(scores)
    scale_Y = (SCREEN_HEIGHT_PXL - 2 * border) / (maximal - minimal + 0.001 )
    i = 0
    for score in scores:
        score = score - minimal
        pygame.draw.line(DISPLAYSURF, RED, (MAP_WIDTH + border + i * scale_X, SCREEN_HEIGHT_PXL - border - previous_cost * scale_Y), (MAP_WIDTH + border + (i+1) * scale_X, SCREEN_HEIGHT_PXL - border - score * scale_Y), line_width)
        i = i + 1
        if not(i % steps):
            myfont = pygame.font.SysFont('Comic Sans', 15)
            textsurface = myfont.render(str(i), False, BLACK)
            DISPLAYSURF.blit(textsurface,(MAP_WIDTH + border + i * scale_X, SCREEN_HEIGHT_PXL - border + 3))
            
            textsurface = myfont.render(str(round(score+minimal,0)), False, BLACK)
            DISPLAYSURF.blit(textsurface,(MAP_WIDTH + border  + i * scale_X + 2, SCREEN_HEIGHT_PXL - border - score * scale_Y + 3))
            
            
        previous_cost = score
        
    myfont = pygame.font.SysFont('Comic Sans', 40)
    textsurface = myfont.render(str(round(maximal,0)), False, BLACK)
    DISPLAYSURF.blit(textsurface,(SCREEN_WIDTH_PXL - 150, SCREEN_HEIGHT_PXL - 50))
    
def Title(DISPLAYSURF, text_to_display):
    myfont = pygame.font.SysFont('Comic Sans', 30)
    textsurface = myfont.render(text_to_display, False, BLACK)
    DISPLAYSURF.blit(textsurface,(2, 15))
    
    
        
        
        
    
        