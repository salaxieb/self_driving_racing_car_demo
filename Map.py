from numpy import *

walls = array([[[0, 0], [50, 0]], [[50, 0], [50, 50]], [[50, 50], [0, 50]], [[0, 50], [0, 0]],
              [[5, 5], [35, 5]],[[35, 5], [45, 15]],[[45, 15], [45, 45]],[[45, 45], [5, 45]],[[5, 45], [5, 5]]])

class Map(object):
    def __init__(self):
        self.walls = walls
        
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
        return sensors_cross_walls
    
    def min_distances(self, sensor):
        return min(self.distances(sensor))
    
    def any_accidents (self, profile):
        for i in profile:
            a = self.min_distances(i)
            if a > 0 and a < 1:
                return True
        return False
    
    def give_score (self, position):
        if position[1]<45 and position[0]>5:
            return sqrt(sum(pow(position,2)))
        if position[1] > 45:
            return sqrt(sum(pow(array([-position[0]+80, position[1]]),2)))
        #if position[0]<5 and position[1]>5:
        #    return sum(pow(array([-position[0]+100, -position[1]+100]),2))
        else:
            return 0