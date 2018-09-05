from __future__ import division
import random
import pygame, sys
from pygame.locals import QUIT
from Car import Car, max_seeing
from drawing import SCREEN_HIGHT_PXL, Draw_Walls
from drawing import SCREEN_WIDTH_PXL
from drawing import WHITE
from numpy import *
#import math
random.seed(1234567890)


walls = array([[[0, 0], [50, 0]], [[50, 0], [50, 50]], [[50, 50], [0, 50]], [[0, 50], [0, 0]],
              [[5, 5], [45, 5]],[[45, 5], [45, 45]],[[45, 45], [5, 45]],[[5, 45], [5, 5]]])
"""
def perp( a ) :
    b = empty_like(a)
    b[:,0] = -a[:,1]
    b[:,1] = a[:,0]
    return b
 
def seg_intersect(a, walls):
    print (a)
    da = a[1]-a[0]
    print ("da", da)
    db = walls[:,1]-walls[:,0]
    print ("db",db)
    print ("a", a[0])
    print ("wall", trsensors_cross_wallspose(walls[:,0], (1,0,2)).shape)
    print ("wall", walls[:,:,0])
    dp = a[:,0] - trsensors_cross_wallspose(walls[:,:,0], (1,0,2))
    print ("dp", dp)
    print ("da", da)
    dap = perp(da)
    print ("dap", dap)
    print ("size", trsensors_cross_wallspose(db, (1,0,2)).shape, dap.T.shape )
    print ("size", db.shape, dap.shape )
    denom = array([])
    for db_i, dap_i in zip(db, dap): #iterating two arrays
        denom = append(denom,dot(db_i, dap_i))
        print ("here",dot(db_i, dap_i))
        print ("there", array(db_i), array(dap_i))
    #denom = dot(trsensors_cross_wallspose(db, (1,0,2)), dap.T).shape
    #denom = 
    print (a.shape[0])
    print (walls.shape[1])
    denom = denom.reshape(a.shape[0],walls.shape[1],1)
    print ("denom",denom)
    print ("denom",denom.shape)
    print (trsensors_cross_wallspose(dp, (1,0,2)).shape, dap.shape)
    num = array([])
    for dp_i, dap_i in zip(trsensors_cross_wallspose(dp, (1,0,2)), dap):
        num = append(num, dot(dp_i, dap_i))
    #num = dot(dp, dap.T)
    num = num.reshape(a.shape[0],walls.shape[1],1)
    print (num.shape)
    print ("num",num)
    print ("div", num / denom.astype(float))
    print ("sizes", (num / denom.astype(float)).shape, db.shape)
    print (walls[:, :,0].shape)
    print ("mult", (multiply((num / denom.astype(float)), db)))
    #print ("sensors_cross_walls", (multiply(num / denom.astype(float), db.T)).T + b[:,0])
    return (multiply((num / denom.astype(float)), db) + walls[:,:,0])

def is_intersect(sensor, walls):
    # y=ax+b
    sensor_a = (sensor[0 ,0] - sensor[1, 0])/(sensor[0, 1] - sensor[1, 1]) #angle tan
    #print ("sensors_a", sensors_a)
    #print ("multiply", multiply(sensors_a, sensors[:, 0, 0]))
    #print ("checks", sensors[:, 0, 1])
    #print ("calcs", sensors[:, 0, 1] - multiply(sensors_a, sensors[:, 0, 0]))
    sensor_b = sensor[0, 1] - multiply(sensor_a, sensor[0, 0])
    print ("sensors_b", sensor_b)
    walls_a = (walls[0, 0] - walls[0, 1]) / (walls[0, 1]-walls[1, 1])
    walls_b = walls[0, 1] - multiply(walls_a, walls [0, 0])
    #print (sensor_a)
    #print (walls[:,0,1])
    #print ((multiply(sensor_a, walls[:,0,0]) + sensor_b > walls[:,0,1]))
    #print (all([multiply(sensor_a, walls[:,0,0]) + sensor_b > walls[:,0,1], multiply(sensor_a, walls[:,0,0]) + sensor_b > walls[:,0,1]], axis=0))
    #print (any([all([multiply(sensor_a, walls[:,0,0]) + sensor_b > walls[:,0,1], multiply(sensor_a, walls[:,0,0]) + sensor_b > walls[:,0,1]], axis=0),
    #            all([multiply(sensor_a, walls[:,0,0]) + sensor_b > walls[:,0,1], multiply(sensor_a, walls[:,0,0]) + sensor_b > walls[:,0,1]], axis=0)],axis = 0))
    
    #intersect = ((multiply(sensor_a, walls[:,0,0]) + sensor_b > walls[:,0,1] and 
                  #multiply(sensor_a, walls[:,1,0]) + sensor_b < walls[:,1,1]) or 
                 #((multiply(sensor_a, walls[:,0,0]) + sensor_b < walls[:,0,1]) and 
                 # (multiply(sensor_a, walls[:, 1, 0]) + sensor_b > walls[:,1,1]))) and 
                 # (((multiply(walls_a, sensor[0, 0]) + walls_b > sensor[0,1] and 
                 #   multiply(walls_a, sensor[0, 1]) + walls_b < sensor[1,1]) or 
                 #  (multiply(walls_a, sensor[0, 0]) + walls_b < sensor[0,1] and 
                 #   multiply(walls_a, sensor[1, 0]) + walls_b > sensor[1,1])))
                
    print (array(sensor_a).size,"aa", array(walls[0,0]).size)
    print ("mult", (array([sensor_a]) * array([walls[0,0]]).T))
    print ("mult", (array([sensor_a]).T * array([walls[0,0]])))
    print (sensor_b)
    print ("sensor_b", array([sensor_a]) * array([walls[0,0]]).T + sensor_b)
    print ("wall", walls[0,1])
    print ("logtest", (array([sensor_a]) * array([walls[0,0]]).T + sensor_b).T > walls[0,1])
    print ("aa",all([(array([sensor_a]) * array([walls[0,0]]).T + sensor_b).T > walls[0,1],
                               (array([sensor_a]) * array([walls[0,0]]).T + sensor_b).T > walls[:,0,1]], axis = 0))
    print ("b",walls_a)
    print (sensor[0, 0])
    print (walls_b)
    #walls_a[isnan(walls_a)] = 0
    #walls_b[isnan(walls_b)] = 0
    print ("cc",array([walls_a]) * array([sensor[0, 0]]).T + walls_b)
    print ((array([walls_a]) * array([sensor[0, 0]]).T + walls_b) > array([sensor[0,1]]).T)
    print ("here", all([array([walls_a]) * array([sensor[0, 0]]).T + walls_b > array([sensor[0,1]]).T,
                          array([walls_a]) * array([sensor[0, 1]]).T + walls_b < array([sensor[1,1]]).T], axis = 0))
    
    #intersect = all([any([all([multiply(sensors_a, walls[:,0,0]) + sensors_b > walls[:,0,1],
    #                           multiply(sensors_a, walls[:,1,0]) + sensors_b < walls[:,1,1]], axis = 0),
    #                 all([multiply(sensors_a, walls[:,0,0]) + sensors_b < walls[:,0,1],
    #                      multiply(sensors_a, walls[:, 1, 0]) + sensors_b > walls[:,1,1]], axis = 0)], axis = 0),
    #                 any([all([multiply(walls_a, sensors[0, 0]) + walls_b > sensors[0,1],
    #                      multiply(walls_a, sensors[0, 1]) + walls_b < sensors[1,1]], axis = 0),
    #                 all([multiply(walls_a, sensors[0, 0]) + walls_b < sensors[0,1],
    #                      multiply(walls_a, sensors[1, 0]) + walls_b > sensors[1,1]], axis = 0)], axis = 0)], axis = 0)
    intersect = all([any([all([(array([sensor_a]) * array([walls[0,0]]).T + sensor_b).T > walls[0,1],
                               (array([sensor_a]) * array([walls[1,0]]).T + sensor_b).T < walls[1,1]], axis = 0),
                     all([(array([sensor_a]) * array([walls[0,0]]).T + sensor_b).T < walls[0,1],
                          (array([sensor_a]) * array([walls[1,0]]).T + sensor_b).T > walls[1,1]], axis = 0)], axis = 0),
                     any([all([array([walls_a]) * array([sensor[0, 0]]).T + walls_b > array([sensor[0,1]]).T,
                          array([walls_a]) * array([sensor[0, 1]]).T + walls_b < array([sensor[1,1]]).T], axis = 0),
                     all([array([walls_a]) * array([sensor[:, 0, 0]]).T + walls_b < array([sensor[0,1]]).T,
                          array([walls_a]) * array([sensor[:, 1, 0]]).T + walls_b > array([sensor[1,1]]).T], axis = 0)], axis = 0)], axis = 0)
    #print ("intersect", intersect)
    return intersect

def min_distances(sensors, walls):
    #sensor[0]
    sensors = array(sensors, "float16")
    walls = array(walls, "float16")
    intersects = is_intersect(sensors, walls) # look for intersections
    print ("intersect", intersects)
    print ("calcs", walls)
    print ("sens", size(sensors, 0))
    print ("calcs", repeat([walls], size(sensors, 0), axis = 0))
    walls = repeat([walls], size(sensors, 0), axis = 0)
    print (walls.shape, intersects.shape)
    walls[logical_not(intersects)] = nan
    print ("calcs", walls)
    b = seg_intersect(sensors, walls) # finds intersection point
    print ("b",b)
    print ("dif", sensors[:, 0] - trsensors_cross_wallspose(b, (1,0,2)))
    print ("power", power(sensors[:, 0] - trsensors_cross_wallspose(b, (1,0,2)),2))
    print ("sum", sum(power(sensors[:,0] - trsensors_cross_wallspose(b, (1,0,2)),2), axis = 2))
    print ("sqrt", sqrt(sum(power(sensors[:,0] - trsensors_cross_wallspose(b, (1,0,2)),2), axis = 2)))
    #distances[isnan(distances)] = max_seeing
    #distances
    #print ("distances", distances)
    distances = sqrt(sum(power(sensors[:,0] - trsensors_cross_wallspose(b, (1,0,2)),2), axis = 2))
    distances[isnan(distances)] = max_seeing
    #print ("ssss", distances.shape)
    #print ("ssss", distances)
    #print (array([], dtype=float64))
    #print ("aa", distances == array([], dtype=float64)) 
    print ("distances", distances)
    print (distances.min(0))
    return distances.min(0)
    #return max_seeing if distances.size == 0 else min(distances)

#print (distance(array([0, 0]), array([4,3])))

p1 = array( [0.0, 0.0] )
p2 = array( [10.0, 10.0] )

p3 = array( [0.0, 12.0] )
p4 = array( [12.0, 0.0] )
p5 = array( [0.0, 6.0] )
p6 = array( [6.0, 0.0] )

#print (seg_intersect(array([p1,p2]), array([[p3,p4],[p5,p6],[p3,p6]])))
#print ("hello!",min_distances(array([[p1, p2],[p3, p2],[p4, p1]]),array([[p3,p4],[p5,p6],[p3,p6],[p2,p6]])))
"""

def min_distances(sensor, walls):
    sensor = array(sensor)
    walls = array(walls)
    #http://www.cs.swan.ac.uk/~cssimon/line_intersection.html
    x1 = sensor[0,0]
    y1 = sensor[0,1]
    x2 = sensor[1,0]
    y2 = sensor[1,1]
    x3 = walls[:,0,0]
    y3 = walls[:,0,1]
    x4 = walls[:,1,0]
    y4 = walls[:,1,1]
    #print ((y3-y4).shape)
    #print ((x1-x3).T.shape)
    #print (dot((y3-y4),(x1-x3).T)+dot((x4-x3),(y1-y3).T))
    #print (dot((y3-y4),(x1-x3))+dot((x4-x3),(y1-y3)))
    a_top = (y3-y4)*(x1-x3)+(x4-x3)*(y1-y3)
    a_bottom = (x4-x3)*(y1-y2)-(x1-x2)*(y4-y3)
    b_top = (y1-y2)*(x1-x3)+(x2-x1)*(y1-y3)
    b_bottom = (x4-x3)*(y1-y2)-(x1-x2)*(y4-y3)
    #print ("top",top)
    #print ("bottom",bottom)
    sensors_cross_walls = a_top/a_bottom
    walls_cross_sensors = b_top/b_bottom
    #print (sensors_cross_walls.shape, walls_cross_sensors.shape)
    sensors_cross_walls[sensors_cross_walls<0] = 1
    sensors_cross_walls[sensors_cross_walls>1] = 1
    sensors_cross_walls[walls_cross_sensors<0] = 1
    sensors_cross_walls[walls_cross_sensors>1] = 1
    #print ("sensors_cross_walls", sensors_cross_walls)
    return (min(sensors_cross_walls))

car = Car()

print ([min_distances(sensor, walls) for sensor in car.sensors()])
intersects = [min_distances(sensor, walls) for sensor in car.sensors()]


pygame.init()
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH_PXL, SCREEN_HIGHT_PXL))
pygame.display.set_caption('Drawing')  

DISPLAYSURF.fill(WHITE)
'''
#nado budet podelit trassu na uchastki chto perischitivat peresecheiya bistree
'''
while True:
    DISPLAYSURF.fill(WHITE)
    Draw_Walls(DISPLAYSURF, walls)
    intersects = [min_distances(sensor, walls) for sensor in car.sensors()]
    car.draw(DISPLAYSURF, True, intersects)
    car.go(0.3, -0.03)
    #sys.exit()
    #car.draw(DISPLAYSURF, False)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    

#
# line segment intersection using vectors
# see Computer Graphics by F.S. Hill
#
