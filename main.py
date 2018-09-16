from __future__ import division
import pygame, sys
from pygame.locals import QUIT
from Car import Car, start_position, sensors_nb, NEURONS_NB
from Map import Map
from Evristic_solution import Evristic
from drawing import SCREEN_HIGHT_PXL, Draw_Walls, Graph
from drawing import SCREEN_WIDTH_PXL
from drawing import WHITE
from numpy import *
from time import time

random.seed(1234567890)


cars = [Car((random.rand((sensors_nb + 3 + 1)*NEURONS_NB + (NEURONS_NB + 1) * 2)-0.5)* 10 * i) for i in range(10)];
map = Map()
solution = Evristic()

pygame.init()
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH_PXL, SCREEN_HIGHT_PXL))
pygame.display.set_caption('Drawing')  

DISPLAYSURF.fill(WHITE)

scores = []


while True:
    DISPLAYSURF.fill(WHITE)
    Draw_Walls(DISPLAYSURF, map.walls)
    new_gen_cars = solution.give_next_generation(cars)
    start = time()
    
    #go = 0.0
    #if pygame.key.get_pressed()[pygame.K_w]:
    #    go = 1.0
    #if pygame.key.get_pressed()[pygame.K_s]:
    #    go = -1.0
    #turn = 0.0
    #if pygame.key.get_pressed()[pygame.K_a]:
    #    turn = 1.0
    #if pygame.key.get_pressed()[pygame.K_d]:
    #    turn = -1.0
    
    
    #my_car.go([go, turn])
    #my_car.go([1.0, 1.0])
    #intersects = [map.min_distances(sensor) for sensor in my_car.sensors()]
    #my_car.go(my_car.brain(intersects))
    #my_car.draw(DISPLAYSURF, not(my_car.in_accident), intersects)
    
    print (new_gen_cars)
    while not(all([car.in_accident for car in new_gen_cars])):
        DISPLAYSURF.fill(WHITE)
        Draw_Walls(DISPLAYSURF, map.walls)
        Graph(DISPLAYSURF, scores)
        for car in new_gen_cars:
            if car.in_accident:
                continue
            intersects = [map.min_distances(sensor) for sensor in car.sensors()]
            car.draw(DISPLAYSURF, not(car.in_accident), intersects)

            if map.any_accidents(car.profile()) or time()-30 > start:
                car.in_accident = True
                car.score = map.give_score(car.position)
                print (car.score)
            else:
                car.go(car.brain(intersects))
            
        pygame.display.update()
    pygame.display.update()
    #cars = solution.selection(cars)
    #print ("ended gen")
    cars = solution.selection(new_gen_cars)
    print ([car.score for car in cars])
    print ("my car resutls", list)
    print ("very end",len(cars))
    scores += [cars[0].score]
    

    for car in cars:
        car.score = 0
        car.position = start_position
        car.in_accident = False
        car.angle = 0
        car.wheels_angle = 0
        car.speed = 0

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    pygame.display.update()
    
