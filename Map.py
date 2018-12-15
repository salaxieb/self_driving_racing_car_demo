from __future__ import division
from numpy import *
import random
from drawing import track_size
from math import tan, asin, sin, cos, atan
from time import time


MAX_ITERATIONS = 1000

#walls = array([[[0, 0], [50, 0]], [[50, 0], [50, 50]], [[50, 50], [0, 50]], [[0, 50], [0, 0]],
#              [[5, 5], [35, 5]],[[35, 5], [45, 15]],[[45, 15], [45, 45]],[[45, 45], [5, 45]],[[5, 45], [5, 5]]])

HALF_ROUTE_WIDTH = 2
min_Y = HALF_ROUTE_WIDTH + 1
max_Y = track_size[1] - HALF_ROUTE_WIDTH - 1


class Map(object):
    def __init__(self, turns = 7, max_angle = 2*pi/3):
        
        self.start = [5, 25]
        self.start_line = [[self.start[0],self.start[1]-HALF_ROUTE_WIDTH],[self.start[0],self.start[1]+HALF_ROUTE_WIDTH]]
        self.finish = [track_size[0]-5,25]
        
        self.walls = []
        
        min_step = 2*HALF_ROUTE_WIDTH
        step = int((self.finish[0]-self.start[0])/(turns+1))
        step = min_step if step < min_step else step
        turning_points = []
        turning_points.append(self.start)
        previous_x = self.start[0]
        previous_y = self.start[1]
        
        for turn in range(turns):
            X = previous_x + random.randint(min_step, step)
            if turn == 0:
                angle = 0
            else:
                angle = random.uniform(-max_angle/2, max_angle/2)
            Y = previous_y + int((X - previous_x)*tan(angle))
            
            Y = min_Y if Y < min_Y else Y
            Y = max_Y if Y > max_Y else Y
            
            turning_points.append([X, Y])
            previous_x = X
            previous_y = Y
            
        turning_points.append(self.finish)
        
        previous_top_wall_end = [self.start[0], self.start[1]-HALF_ROUTE_WIDTH]
        previous_bottom_wall_end = [self.start[0], self.start[1]+HALF_ROUTE_WIDTH]
        top_wall_end = 0
        bottom_wall_end = 0
        
        #angle - route angle
        #delta - normal distance from route center to angle
        #bissectrice - angle of current delta gap
        
        for this_dot in range(len(turning_points)-2):
            next_dot = this_dot+1
            this_angle = atan((-turning_points[next_dot][1] + turning_points[this_dot][1])/(turning_points[next_dot][0] - turning_points[this_dot][0]))
            if next_dot+2 < len(turning_points):
                next_angle = atan((-turning_points[next_dot+1][1] + turning_points[next_dot][1])/(turning_points[next_dot+1][0] - turning_points[next_dot][0]))
            else:
                next_angle = 0
            bissectrice = (this_angle + next_angle + pi)/2
            delta = HALF_ROUTE_WIDTH / sin(pi - bissectrice + this_angle)
            top_wall_end = [turning_points[next_dot][0] + delta * cos(bissectrice), turning_points[next_dot][1] - delta * sin(bissectrice)]
            bottom_wall_end = [turning_points[next_dot][0] - delta * cos(bissectrice), turning_points[next_dot][1] + delta * sin(bissectrice)]
            self.walls.append([previous_top_wall_end, top_wall_end])
            self.walls.append([previous_bottom_wall_end, bottom_wall_end])
            previous_top_wall_end = top_wall_end
            previous_bottom_wall_end = bottom_wall_end
            
        self.finish = array(top_wall_end) + (array(bottom_wall_end) - array(top_wall_end))/2 + array([4,0])
        self.finish_line = [[self.finish[0],self.finish[1]-HALF_ROUTE_WIDTH],[self.finish[0],self.finish[1]+HALF_ROUTE_WIDTH]]
        self.walls.append([top_wall_end,[self.finish[0], self.finish[1]-HALF_ROUTE_WIDTH]])
        self.walls.append([bottom_wall_end,[self.finish[0], self.finish[1]+HALF_ROUTE_WIDTH]])
        
#         self.walls.append(self.finish_line + array([[0.3,0],[0.3,0]])) #wall in the end
        self.walls.append(array(self.start_line) + array([[-2.1,0],[-2.1,0]]))
            
        
        
    def distances(self, sensor):
        sensor = array(sensor)
        walls = array(self.walls)
        #http://www.cs.swan.ac.uk/~cssimon/line_intersection.html
        x1 = sensor[0,0]
        y1 = sensor[0,1]
        x2 = sensor[1,0]
        y2 = sensor[1,1]
        x3 = walls[:,0,0]
        y3 = walls[:,0,1]
        x4 = walls[:,1,0]
        y4 = walls[:,1,1]

        a_top = (y3-y4)*(x1-x3)+(x4-x3)*(y1-y3)
        a_bottom = (x4-x3)*(y1-y2)-(x1-x2)*(y4-y3)
        b_top = (y1-y2)*(x1-x3)+(x2-x1)*(y1-y3)
        b_bottom = (x4-x3)*(y1-y2)-(x1-x2)*(y4-y3)

        sensor_cross_walls = a_top/a_bottom
        walls_cross_sensor = b_top/b_bottom

        sensor_cross_walls[sensor_cross_walls<0] = 1
        sensor_cross_walls[sensor_cross_walls>1] = 1
        sensor_cross_walls[walls_cross_sensor<0] = 1
        sensor_cross_walls[walls_cross_sensor>1] = 1
        sensor_cross_walls[sensor_cross_walls == nan] = 1

        return sensor_cross_walls #result [0;1] if sensor crosses wall
    
    def distances_to_sensors(self, sensors):
        sensors = array(sensors)
        #pp.pprint (shape(self.walls))
        wall_shape = shape(self.walls)
        walls = broadcast_to(self.walls, (len(sensors),wall_shape[0],wall_shape[1],wall_shape[2]))
        #pp.pprint (shape(walls))
        #pp.pprint (walls)
        #http://www.cs.swan.ac.uk/~cssimon/line_intersection.html
        x1 = sensors[:,0,0]
        y1 = sensors[:,0,1]
        x2 = sensors[:,1,0]
        y2 = sensors[:,1,1]
        x3 = walls[:,:,0,0]
        y3 = walls[:,:,0,1]
        x4 = walls[:,:,1,0]
        y4 = walls[:,:,1,1]
        
        a_top = (y3-y4)*transpose(subtract(x1,transpose(x3)))+(x4-x3)*transpose(subtract(y1,transpose(y3)))
        a_bottom = transpose(multiply(transpose(x4-x3),(y1-y2)))-transpose(multiply(transpose(y4-y3),(x1-x2)))
        b_top = transpose(multiply(subtract(x1,transpose(x3)),(y1-y2)))+transpose(multiply(subtract(y1,transpose(y3)),(x2-x1)))
        b_bottom = a_bottom
        sensor_cross_walls = a_top/a_bottom
        walls_cross_sensor = b_top/b_bottom

        sensor_cross_walls[sensor_cross_walls<0] = 1
        sensor_cross_walls[sensor_cross_walls>1] = 1
        sensor_cross_walls[walls_cross_sensor<0] = 1
        sensor_cross_walls[walls_cross_sensor>1] = 1

        return sensor_cross_walls #result [0;1] if sensor crosses wall
    
    def min_distances(self, sensors):
        return amin(self.distances_to_sensors(sensors),axis=1)
    
    def any_accidents_or_finished (self, car):
        if car.position[0] > self.finish[0]:
            car.finished = True
        a = self.min_distances(car.profile())
        if (min(a) > 0 and min(a) < 1) or (car.finished):
            return True
        return False
    
    def give_score (self, car, iteration):
#         distance_score = sqrt(sum(pow(car.position,2)))
        distance_score = car.position[0]
        speed_score = 0
        if car.finished:
            speed_score = MAX_ITERATIONS - iteration
        return distance_score + speed_score
#         if position[1]<45 and position[0]>5:
#             return sqrt(sum(pow(position,2)))
#         if position[1] > 45:
#             return sqrt(sum(pow(array([-position[0]+80, position[1]]),2)))
#         #if position[0]<5 and position[1]>5:
#         #    return sum(pow(array([-position[0]+100, -position[1]+100]),2))
#         else:
#             return 0