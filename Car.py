#from main import car_mass, car_power, max_turning_angle, max_turning_speed, base_length, base_width, sensors_nb, sensors_angle, L, W
import pygame
from drawing import FPS, BLACK, DRAW_SCALE, GREEN, GREY, RED
from Map import Map
#from math import pi, sin, cos
from numpy import *
from time import time

#car parameters: 
car_mass = 500#kg
car_power = 12000#wt,  max a = 5m/s
max_speed = 2 #m/s = 100km/h
max_turning_angle = pi/6 #30 degrees
max_turning_speed = pi/3 #in a second
#base_length = 1.5#m
#base_width = 1#m
sensors_nb = 20 #car eyes nb
sensors_angle = pi*5/4 #sensors don't look back
max_seeing = 8#m
L = 2.0#m
W = 1.0#m
start_pos = [5-1, 2.5]
NEURONS_NB = 100
LAMBD = 0.001

def sigmoid(a):
    return 2/(1+exp(-a))-1 #[-1;1]

def relu(a):
    a[a<0] = 0
    return a

def sigmoid_gradient(a):
    return 2/(1+exp(negative(a)))*(1-1/(1+exp(negative(a))))

def relu_gradient(a):
    a[a > 0] = 1
    a[a <= 0] = 0
    return a

def evaluate(inpt, Theta_1, Theta_2):
        #Theta_1 = self.get_theta1()
        #Theta_2 = self.get_theta2()
        
#         print ("input",shape(inpt))
        z_1 = a_1 = append(ones((shape(inpt)[0],1)), inpt, axis=1)
#         print ("a_1", shape(a_1))
#         print ("T1", shape(Theta_1))
        z_2 = dot(a_1,Theta_1)
#         print ("z_2", shape(z_2))
        a_2 = relu(z_2) #relu
#         print ("a_2", shape(a_2))
        a_2 = append(ones((shape(a_2)[0],1)), a_2, axis=1)
#         print ("a_2", shape(a_2))
#         print ("T_2", shape(Theta_2))
        z_3 = dot(a_2, Theta_2)
#         print ("z_3", shape(z_3))
        out = sigmoid(z_3) #softmax
#         print ("out", shape(out))
        return out, z_1, z_2, z_3, a_1, a_2
    
def cost(inpt, Y, Theta_1, Theta_2):
    
    h, z_1, z_2,z_3, a_1, a_2 = evaluate(inpt, Theta_1, Theta_2)
    
    m = shape(h)[0]
    sum_theta = 0
    sum_theta += sum(sum(dot(Theta_1[1:,:].T,Theta_1[1:,:]))) #droppping bias
    sum_theta += sum(sum(dot(Theta_2[1:,:].T,Theta_2[1:,:])))
#     print (shape(h))
#     print (Y)
#     a = negative(Y) * log(h) - (ones(shape(Y)) - Y) * log(ones(shape(h)) - h);
#     J = 1/m * sum(sum(a)) + LAMBDa/(2*m)*(sum(sum(Theta1(:,2:end) .^2))+sum(sum(Theta2(:,2:end) .^2)));
    return sum(sum(power((h-Y),2)))/(2*m) + LAMBD/(2*m)*sum_theta
# return 1./m *sum(sum(a))

class Car(object):
    def __init__(self, gen = (random.rand((sensors_nb + 3 + 1)*NEURONS_NB + (NEURONS_NB + 1) * 2) - 0.5), start_position = start_pos):# - 0.48)):
        self.mass = car_mass
        self.power = car_power
        self.max_angle = max_turning_angle
        self.turning_speed = max_turning_speed
        self.in_accident = False
        self.gen = gen
        self.sensors_angles = []
        self.is_leader = False
        for i in range(sensors_nb):
            self.sensors_angles.append(-sensors_angle/2 + i * sensors_angle/(sensors_nb-1))
        self.reset(start_position)
        
    def draw(self, DISPLAYSURF, intersects):
        X = self.position[0] - L * cos(self.angle) - W/2 * sin(self.angle) #X and Y top left point of car
        Y = self.position[1] + L * sin(self.angle) - W/2 * cos(self.angle)
        draw_color = BLACK if self.is_leader else GREY
        for line in self.profile():
            pygame.draw.line(DISPLAYSURF, draw_color, line[0]*DRAW_SCALE, line[1]*DRAW_SCALE, 2)

        pygame.draw.line(DISPLAYSURF, draw_color, [(X + L/2 * cos(self.angle) + W/2 * sin(self.angle))*DRAW_SCALE, (Y - L/2 * sin(self.angle) + W/2 * cos(self.angle))*DRAW_SCALE],
                                              [(X + L * cos(self.angle) + W/2 * sin(self.angle))*DRAW_SCALE, (Y - L * sin(self.angle) + W/2 * cos(self.angle))*DRAW_SCALE], 3)
        for sensor, distance in zip(self.sensors(),intersects):
            pygame.draw.line(DISPLAYSURF, GREEN, sensor[0]*DRAW_SCALE, sensor[1]*DRAW_SCALE, 1)
#             print (distance)
#             print (sensor[0])
#             print (sensor[1])
            circle = array(sensor[0]+(sensor[1]-sensor[0])*distance)
            if any(isnan(circle==nan)):
                print ("AAAAAAAAAAA", circle)
            circle[isnan(circle)] = max_seeing
            pygame.draw.circle(DISPLAYSURF, RED, circle*DRAW_SCALE, 2)

    def sensors(self):
        a = array(sensors_nb * [[self.position, self.position]], float16)
        a[:,1,0] += multiply(max_seeing, cos(self.angle + array(self.sensors_angles)))
        a[:,1,1] += multiply(max_seeing, -sin(self.angle + array(self.sensors_angles)))
        return a
    
    def profile(self):
        X = self.position[0] - L * cos(self.angle) - W/2 * sin(self.angle) #X and Y top left point of car
        Y = self.position[1] + L * sin(self.angle) - W/2 * cos(self.angle)
        return array([[[X, Y],
                 [X + L * cos(self.angle),Y - L * sin(self.angle)]],
                [[X + L * cos(self.angle), Y - L * sin(self.angle)],
                 [X + L * cos(self.angle) + W * sin(self.angle), Y - L * sin(self.angle) + W * cos(self.angle)]],
                [[X + L * cos(self.angle) + W * sin(self.angle), Y - L * sin(self.angle) + W * cos(self.angle)],
                 [X + W * sin(self.angle), Y + W * cos(self.angle)]],
                [[X + W * sin(self.angle), Y + W * cos(self.angle)],
                 [X, Y]]])
        
    
    def go(self,inpt):
#         print (inpt)
        #power (-1,1) - percentage of implemented power
        #angle (-1,1) - percentage of turning angle speed
        inpt = inpt[0]
        forward = inpt[0]
#         print (inpt[1])
        left = inpt[1]
        
        self.speed += forward*max_speed/FPS
        self.wheels_angle = max_turning_angle * left
        
        self.angle += arcsin((self.speed/FPS * sin(self.wheels_angle))/L)
        self.position += self.speed/FPS * array([cos(self.angle), -sin(self.angle)])
        
#     def go_old(self, inpt):
#         gas_pedal = inpt[0]
#         stearing_wheel = inpt[1]
#         #power (-1,1) - percentage of implemented power
#         #angle (-1,1) - percentage of turning angle speed
#         if self.speed > 1 and self.speed < max_speed:
#             self.speed += (gas_pedal*self.power)/(self.mass*self.speed)/FPS
#         elif self.speed >= max_speed and gas_pedal < 0:
#             self.speed += (gas_pedal*self.power)/(self.mass)/FPS
#         elif self.speed <= 1:
#             self.speed += (gas_pedal*self.power)/(self.mass)/FPS
#         else:
#             pass
#         
#         if abs(self.wheels_angle) < max_turning_angle:
#             self.wheels_angle += (stearing_wheel*self.turning_speed/FPS)
#         
#         self.angle += arcsin((self.speed/FPS * sin(self.wheels_angle))/L)
#         
#         self.position += self.speed/FPS * array([cos(self.angle), -sin(self.angle)])
    
    def get_inputs(self, intersects):
        # input (sensors_nb + speed + wheels_angle + angle) #[-1; 1]
        # 3 layer perceptrone with neurons=input+10  - relu !
        # output (power, stearing_wheel) - softmax ! # (-1; 1)
        return append(intersects, [self.speed/max_speed, self.wheels_angle/max_turning_angle, self.angle/(2*pi)])
    
    def theta_deliminiter(self):
        return (sensors_nb + 3 + 1)*NEURONS_NB
    def get_theta1(self):
        return copy(self.gen[:self.theta_deliminiter()].reshape((sensors_nb + 3 + 1, NEURONS_NB)))    #+bias size = (15, 10)
    def get_theta2(self):
        return copy(self.gen[self.theta_deliminiter():].reshape((NEURONS_NB + 1, 2)))                 #+bias size = (11, 2)
    def set_theta1(self, theta1):
        self.gen[:self.theta_deliminiter()] = copy(theta1.flatten())
    def set_theta2(self, theta2):
        self.gen[self.theta_deliminiter():] = copy(theta2.flatten())
        
        
    def brain(self, intersects):
        inpt = self.get_inputs(intersects)
        
        out, z_1, z_2, z_3, a_1, a_2 = evaluate([inpt], self.get_theta1(), self.get_theta2())
        return out
    
    def get_gradient(self, X_train, Y_train, Theta_1, Theta_2):
        evaluation,z_1,z_2,z_3, a_1, a_2 = evaluate(X_train, Theta_1, Theta_2)
        m = shape(evaluation)[0]
    
        delta_3 = (evaluation - Y_train)*sigmoid_gradient(z_3)
    #         print ("delta 3", shape(delta_3))
    #         print ("Thet 2.T", shape(Theta_2.T))
    #         print ("D2 shape", shape(dot(a_2.T,delta_3)))
    # #         D2 =  1./m*(dot(a_2.T,delta_3) + LAMBD*Theta_2)
    #         print ("shape h", shape(sigmoid_gradient(z_3)))
    #         print ("shape a_2", shape(a_2))
        D2 = dot(a_2.T, delta_3)/m
    #         Theta_2 = Theta_2[1:,:]
        delta_2 = dot(delta_3, Theta_2.T) * relu_gradient(append(ones((shape(z_2)[0],1)), z_2, axis=1))
    #         print ("Thet 2.T", shape(Theta_2.T))
    #         print ("Z_2", shape(z_2))
    #         print ("dot shape", shape(dot(delta_3, Theta_2.T)))
    #         print ("delta 2", shape(delta_2))
    #         
    #         Theta_2[0:1,:]=0 #not normiizing bias
        
    #         delta_2 = delta_2[:,1:] #dropping bias
    #         print ("delta_2", shape(delta_2))
    #         print ("theta 1", shape(Theta_1))
    #         print ("z_1", shape(z_1))
        delta_2 = delta_2[:,1:]
        D1 = (dot(z_1.T,delta_2))/m
    #         Theta_1 = Theta_1[1:,:]
    #         delta_1 = dot(delta_2, Theta_1.T) * sigmoid_gradient(z_1)
    #         print ("delta_1", shape(delta_1))
    #         Theta_1[0:1,:]=0
        return D1, D2
        
    def train_brain(self, X_train, Y_train,  X_test = NaN, Y_test = NaN, alpha = 0.5, epochs = 500):
        Theta_1 = self.get_theta1()
        Theta_2 = self.get_theta2()
        m = shape(X_train)[0]
        J = []
        J_test = []
        for i in range(epochs):
            D1, D2 = self.get_gradient(X_train, Y_train, Theta_1, Theta_2)
            Theta_1 = Theta_1 - alpha*D1 - LAMBD/(2*m)
            Theta_2 = Theta_2 - alpha*D2 - LAMBD/(2*m)
            J.append(cost(X_train, Y_train, Theta_1, Theta_2))
            J_test.append(cost(X_test, Y_test, Theta_1, Theta_2))
                
        self.set_theta1(Theta_1)
        self.set_theta2(Theta_2)
        return J, J_test  
    
    def reset(self, start):
        self.score = 0
        self.position = start
        self.in_accident = False
        self.finished = False
        self.angle = 0
        self.wheels_angle = 0
        self.speed = 0
        self.start_time = time()
