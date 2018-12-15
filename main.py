from __future__ import division
import pygame, sys
from pygame.locals import QUIT
from Car import Car, start_pos, sensors_nb, NEURONS_NB
from Map import Map, MAX_ITERATIONS
from Evristic_solution_no_class import give_next_generation, selection, max_cars
from drawing import SCREEN_HEIGHT_PXL, Draw_Map, Graph, Title
from drawing import SCREEN_WIDTH_PXL
from drawing import WHITE
from numpy import *
import numpy as np
from time import time
import csv

NUMBER_OF_MAPS = 3


random.seed(12345678)

def write_to_CSV(data):
    #data = ["1","1","1","1","1"]
    np.save("training_data_d", data)           
    print ("finished")
    return ("training_data.csv")

def get_data():
    
    data = load("training_data_d" + '.npy', encoding="latin1")
    print ("this race data", shape(data))
    if shape(data)[1] == 0:
        data = load("training_data_c" + '.npy', encoding="latin1")
    print (shape(data))
    X = data[0][0]
    X = list(X)
#     random.shuffle(X)
    Y = data[1][0]
    Y = list(Y)

#     Y[:][Y<0.5] = 0.5
    train_test_split = int(0.7*shape(X)[0])
    
    X_train = X[:train_test_split]
#     X_train = ones(shape(X_train))
    X_test= X[train_test_split:]
    
    Y_train = Y[:train_test_split]
    Y_test= Y[train_test_split:]

    return X_train, X_test, Y_train, Y_test
    
    
def manual_drive(maps):
    temporary_input_training_data = []
    temporary_output_training_data = []
    
    input_training_data = []
    output_training_data = []
    
    results = zeros(len(maps))
    i = -1
#     map = Map(int(random.triangular(max_turns/3, max_turns, max_turns))
#               ,random.triangular(max_angle/3, max_angle, max_angle))
    for map in maps:
        my_car = Car()
        my_car.is_leader = True
        my_car.reset(map.start)
        iteration = 0
        i += 1
        
        while not(pygame.key.get_pressed()[pygame.K_q] or my_car.finished == True):
            iteration += 1
            DISPLAYSURF.fill(WHITE)
            Title(DISPLAYSURF, str(i+1)+" of "+str(NUMBER_OF_MAPS))
            go = 0.0
            turn = 0.0
            if pygame.key.get_pressed()[pygame.K_w]:
                go = 1.0
            if pygame.key.get_pressed()[pygame.K_s]:
                go = -1.0
            if pygame.key.get_pressed()[pygame.K_a]:
                turn = 1.0
            if pygame.key.get_pressed()[pygame.K_d]:
                turn = -1.0
            
            
            my_car.go([[go, turn]])
            intersects = map.min_distances(my_car.sensors())
            Draw_Map(DISPLAYSURF, map, MAX_ITERATIONS-iteration)
            my_car.draw(DISPLAYSURF, intersects)
            
            temporary_input_training_data.append(my_car.get_inputs(intersects))
            temporary_output_training_data.append([go, turn])
    
            
            if map.any_accidents_or_finished(my_car):
                if my_car.finished:
                    results[i] = map.give_score(my_car, iteration)
                    print (temporary_output_training_data)
                    input_training_data.append(temporary_input_training_data)
                    output_training_data.append(temporary_output_training_data)
                else:
                    my_car.reset(map.start)
                iteration = 0
                temporary_input_training_data = []
                temporary_output_training_data = []
                               
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            
    write_to_CSV([input_training_data, output_training_data])
        
    return results

def do_evolution_sycles(maps, cars, scores):
    new_gen_cars = give_next_generation(cars)
    iteration = 0
    
    this_iter_best_score = zeros(len(maps))
    cars_scores = zeros((len(maps),len(new_gen_cars)))
    map_iter = 0
    for map in maps:
        for car in new_gen_cars:
            car.reset(map.start)
            
        while not(all([car.in_accident for car in new_gen_cars])):
            iteration += 1
            DISPLAYSURF.fill(WHITE)
            Draw_Map(DISPLAYSURF, map, MAX_ITERATIONS - iteration)
            Graph(DISPLAYSURF, scores)
            for car in new_gen_cars:
                if car.in_accident:
                    continue
                intersects = map.min_distances(car.sensors())
                car.draw(DISPLAYSURF, intersects)
    
                if map.any_accidents_or_finished(car) or iteration > MAX_ITERATIONS:
                    car.in_accident = True
                    car.score = map.give_score(car, iteration)
                    #print (car.score)
                else:
                    car.go(car.brain(intersects))
                
            pygame.display.update()
        cars_scores[map_iter] = [car.score for car in new_gen_cars]
        map_iter += 1
#     cars = solution.selection(cars)
    #print ("ended gen")
#     b_score = 0
#     for car in new_gen_cars:
#         if car.score > b_score:
#             best_gen = i.gen
#             b_score = i.score
    print (cars_scores)
    print (average(cars_scores, axis = 0))
    for i in range(len(new_gen_cars)-1):
        new_gen_cars[i].score = average(cars_scores, axis = 0)[i]
    cars = selection(new_gen_cars)
    this_iter_best_score = cars[0].score
    #print ([car.gen for car in cars])
#     print (shape(scores))
#     print (len(scores[i]))
#     scores[i][-1] = cars[0].score
    

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    pygame.display.update()
    return cars, this_iter_best_score

map = Map()
cars = [Car((random.rand((sensors_nb + 3 + 1)*NEURONS_NB + (NEURONS_NB + 1) * 2)-0.5), map.start) for i in range(max_cars)];
pygame.init()
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH_PXL, SCREEN_HEIGHT_PXL))
pygame.display.set_caption('Drawing')  

DISPLAYSURF.fill(WHITE)
max_angle = 2*pi/3
max_turns = 7
maps = [Map(int(random.triangular(max_turns/3, max_turns, max_turns))
            ,random.triangular(max_angle/3, max_angle, max_angle)) for i in range(NUMBER_OF_MAPS)]

results = manual_drive(maps)

X_train, X_test, Y_train, Y_test = get_data()
J = array([])
# i = 0
# for car in cars:
#     i += 1
#     Title(DISPLAYSURF, str(i) + " of " + str(10))
#     J = append(J, car.train_brain(X_train, Y_train,  X_test, Y_test))
J = array([car.train_brain(X_train, Y_train,  X_test, Y_test) for car in cars])
print (shape(J))
print ("final J/J_test equals:",J[:,0,-1]/J[:,1,-1])
scores = []
while True:    
#     map = Map(int(random.triangular(max_turns/3, max_turns, max_turns))
#              ,random.triangular(max_angle/3, max_angle, max_angle))  
    cars, this_iter_score = do_evolution_sycles(maps, cars, scores)
    scores = append(scores, average(this_iter_score))
    
    print (shape(scores))
    print (scores)
    
    
