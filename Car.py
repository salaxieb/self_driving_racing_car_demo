#from main import car_mass, car_power, max_turning_angle, max_turning_speed, base_length, base_width, sensors_nb, sensors_angle, L, W
import pygame
from drawing import BLACK, DRAW_SCALE, GREEN, GREY
#from math import pi, sin, cos
from numpy import *

#car parameters: 
car_mass = 500#kg
car_power = 12000#wt,  max a = 5m/s
max_turning_angle = pi/6 #30 degrees
max_turning_speed = pi/12 #in a second
base_length = 1.5#m
base_width = 1#m
sensors_nb = 4 #car eyes nb
sensors_angle = pi #sensors don't look back
max_seeing = 15#m
L = 2.0#m
W = 1.0#m
start_position = [5-1, 2.5]


class Car(object):
    def __init__(self):
        self.mass = car_mass
        self.power = car_power
        self.max_angle = max_turning_angle
        self.turning_speed = max_turning_speed
        self.speed = 0
        self.wheels_angle = 0
        self.position = start_position
        self.angle = 0
        self.sensors_angles = []
        for i in range(sensors_nb):
            self.sensors_angles.append(-sensors_angle/2 + i * sensors_angle/(sensors_nb-1))
        
    def draw(self, DISPLAYSURF, is_main):
        X = self.position[0] - L #X and Y top left point of car
        Y = self.position[1] - W/2
        draw_color = BLACK if is_main else GREY
        pygame.draw.lines(DISPLAYSURF, draw_color, True, [[X * DRAW_SCALE, Y * DRAW_SCALE], 
                                               [(X + L * cos(self.angle))*DRAW_SCALE, (Y - L * sin(self.angle))*DRAW_SCALE],
                                               [(X + L * cos(self.angle) + W * sin(self.angle))*DRAW_SCALE, (Y - L * sin(self.angle) + W * cos(self.angle))*DRAW_SCALE],
                                               [(X + W * sin(self.angle))*DRAW_SCALE, (Y + W * cos(self.angle))*DRAW_SCALE]], 3)
        
        pygame.draw.line(DISPLAYSURF, draw_color, [(X + L/2 * cos(self.angle) + W/2 * sin(self.angle))*DRAW_SCALE, (Y - L/2 * sin(self.angle) + W/2 * cos(self.angle))*DRAW_SCALE],
                                              [(X + L * cos(self.angle) + W/2 * sin(self.angle))*DRAW_SCALE, (Y - L * sin(self.angle) + W/2 * cos(self.angle))*DRAW_SCALE], 3)
        
        for i in self.sensors_angles:
            pygame.draw.line(DISPLAYSURF, GREEN, [(X + L * cos(self.angle) + W/2 * sin(self.angle))*DRAW_SCALE, 
                                                  (Y - L * sin(self.angle) + W/2 * cos(self.angle))*DRAW_SCALE],
                                              [(X + L * cos(self.angle) + W/2 * sin(self.angle) + max_seeing * cos(self.angle + i))*DRAW_SCALE, 
                                               (Y - L * sin(self.angle) + W/2 * cos(self.angle) - max_seeing * sin(self.angle + i))*DRAW_SCALE], 1)
    
    def sensors(self):
        #a = zeros([sensors_nb,2,2], float16)
        #print (sensors_nb * [[self.position, self.position]])
        a = array(sensors_nb * [[self.position, self.position]], float16)
        #j = 0
        #for i in self.sensors_angles:
        #    a[j] = [self.position, self.position + multiply(max_seeing, [cos(self.angle + i), -sin(self.angle + i)])]
        #    j+=1
        #print (a)
        #print (a[:,1,1])
        #print(multiply(max_seeing, [cos(self.angle + array(self.sensors_angles)), -sin(self.angle + array(self.sensors_angles))]))
        #print (a[:,1,0] + multiply(max_seeing, cos(self.angle + array(self.sensors_angles))))
        #print (a[:,1,1] + multiply(max_seeing, -sin(self.angle + array(self.sensors_angles))))
        a[:,1,0] += multiply(max_seeing, cos(self.angle + array(self.sensors_angles)))
        a[:,1,1] += multiply(max_seeing, -sin(self.angle + array(self.sensors_angles)))
        #print (a)
        return a
            
        
                                                                            
