#from main import car_mass, car_power, max_turning_angle, max_turning_speed, base_length, base_width, sensors_nb, sensors_angle, L, W
import pygame
from drawing import FPS, BLACK, DRAW_SCALE, GREEN, GREY, RED
#from math import pi, sin, cos
from numpy import *

#car parameters: 
car_mass = 500#kg
car_power = 12000#wt,  max a = 5m/s
max_speed = 27.8 #m/s = 100km/h
max_turning_angle = pi/6 #30 degrees
max_turning_speed = pi/12 #in a second
#base_length = 1.5#m
#base_width = 1#m
sensors_nb = 50 #car eyes nb
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
        
    def draw(self, DISPLAYSURF, is_main, intersects):
        X = self.position[0] - L * cos(self.angle) - W/2 * sin(self.angle) #X and Y top left point of car
        Y = self.position[1] + L * sin(self.angle) - W/2 * cos(self.angle)
        print ([X,Y],"aA", self.position)
        draw_color = BLACK if is_main else GREY
        pygame.draw.lines(DISPLAYSURF, draw_color, True, [[X * DRAW_SCALE, Y * DRAW_SCALE], 
                                               [(X + L * cos(self.angle))*DRAW_SCALE, (Y - L * sin(self.angle))*DRAW_SCALE],
                                               [(X + L * cos(self.angle) + W * sin(self.angle))*DRAW_SCALE, (Y - L * sin(self.angle) + W * cos(self.angle))*DRAW_SCALE],
                                               [(X + W * sin(self.angle))*DRAW_SCALE, (Y + W * cos(self.angle))*DRAW_SCALE]], 3)
        
        pygame.draw.line(DISPLAYSURF, draw_color, [(X + L/2 * cos(self.angle) + W/2 * sin(self.angle))*DRAW_SCALE, (Y - L/2 * sin(self.angle) + W/2 * cos(self.angle))*DRAW_SCALE],
                                              [(X + L * cos(self.angle) + W/2 * sin(self.angle))*DRAW_SCALE, (Y - L * sin(self.angle) + W/2 * cos(self.angle))*DRAW_SCALE], 3)
        for sensor, distance in zip(self.sensors(),intersects):
            pygame.draw.line(DISPLAYSURF, GREEN, sensor[0]*DRAW_SCALE, sensor[1]*DRAW_SCALE, 1)
            pygame.draw.circle(DISPLAYSURF, RED, (sensor[0]+(sensor[1]-sensor[0])*distance)*DRAW_SCALE, 2)
        
        #for i in self.sensors_angles:
        #    pygame.draw.line(DISPLAYSURF, GREEN, [(X + L * cos(self.angle) + W/2 * sin(self.angle))*DRAW_SCALE, 
        #                                          (Y - L * sin(self.angle) + W/2 * cos(self.angle))*DRAW_SCALE],
        #                                      [(X + L * cos(self.angle) + W/2 * sin(self.angle) + max_seeing * cos(self.angle + i))*DRAW_SCALE, 
        #                                       (Y - L * sin(self.angle) + W/2 * cos(self.angle) - max_seeing * sin(self.angle + i))*DRAW_SCALE], 1)
    
    def sensors(self):
        a = array(sensors_nb * [[self.position, self.position]], float16)
        a[:,1,0] += multiply(max_seeing, cos(self.angle + array(self.sensors_angles)))
        a[:,1,1] += multiply(max_seeing, -sin(self.angle + array(self.sensors_angles)))
        return a
    
    def go(self, gas_pedal, stearing_wheel):
        #power (-1,1) - percentage of implemented power
        #angle (-1,1) - percentage of turning angle speed
        if self.speed > 1 and self.speed < max_speed:
            self.speed += (gas_pedal*self.power)/(self.mass*self.speed)/FPS
        elif self.speed >= max_speed and gas_pedal < 0:
            self.speed += (gas_pedal*self.power)/(self.mass)/FPS
        elif self.speed <= 1:
            self.speed += (gas_pedal*self.power)/(self.mass)/FPS
        else:
            pass
            
        
        if abs(self.wheels_angle) < max_turning_angle:
            self.wheels_angle += (stearing_wheel*self.turning_speed/FPS)
        
        self.angle += arcsin((self.speed/FPS * sin(self.wheels_angle))/L)
        
        self.position += self.speed/FPS * array([cos(self.angle), -sin(self.angle)])
        
        #print (self.angle, self.position, self.speed, self.wheels_angle)
        
                
        return
    
        
        
                                                                            
