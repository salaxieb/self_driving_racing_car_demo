
from numpy import *
from Car import Car, sensors_nb, NEURONS_NB
from copy import deepcopy#, copy
X_points = 3
to_mutation = 0.4
max_cars = 10


class Evristic():
    
    def __init__(self):
        self.iter = 0
        self.update_lambda()
    
    def give_next_generation(self, cars):
        for car in cars:
            print ("tall",car.gen[:3])
        new_cars = self.mutation(cars)#[:int(to_mutation * len(cars))])
        #new_cars += self.crossbreeding(cars)#[int(to_mutation * len(cars)):])
        #print (new_cars)
        #cars = self.check_for_repeats(cars+new_cars)
        #return cars+new_cars
        [cars.append(new_car) for new_car in new_cars]
        return cars
    
    def update_lambda(self):
        if self.iter < 360:
            self.iter += 1
        self.lmbd = exp(-300.0/(400.0-self.iter))
        
    
    def mutation(self, old_cars):
        self.update_lambda()
        new_cars=[]
        for old_car in old_cars:
            new_cars.append(Car(old_car.gen.copy()))
            #new_cars.append(Car((random.rand((sensors_nb + 3 + 1)*NEURONS_NB + (NEURONS_NB + 1) * 2)-0.5)* 30))
            
        self.check_for_repeats(new_cars)
        for car in new_cars:
            a = array(random.uniform(-self.lmbd, self.lmbd, len(car.gen)))
            car.gen += multiply(car.gen, a)
        return new_cars
            
    
    def crossbreeding(self, old_cars):
        new_cars = deepcopy(old_cars)
        for car in new_cars:
            print ("beg",car.gen[:3])
        if len(new_cars) % 2 == 1:
            new_cars.pop()
        for i in range(len(new_cars)):
            if i % 2 == 1:
                continue
            for iter in range(X_points):
                point = random.randint(2, len(new_cars[i].gen-1))
                #print (point)
                #temp = copy(new_cars[i+1].gen[:point])
                #print (new_cars[i].gen[:3])
                #new_cars[i+1].gen[:point] = copy(new_cars[i].gen[:point])
                #new_cars[i].gen[:point] = copy(temp)
                new_cars[i].gen[:point], new_cars[i+1].gen[:point] = new_cars[i+1].gen[:point].copy(), new_cars[i].gen[:point].copy()
                #new_cars[i].gen[:point], new_cars[i+1].gen[:point] = new_cars[i+1].gen[:point], new_cars[i].gen[:point]
        for car in new_cars:
            print (car.gen[:3])
        return new_cars
                
    def shuffle(self,cars):

        for i in range(len(cars)-1):
            j = random.randint(i, len(cars)-1)
            tmp = deepcopy(cars[i])
            cars[i] = deepcopy(cars[j])
            cars[j] = deepcopy(tmp)
        return cars
    
    def sort_by_score(self,car):
        return car.score
    
    def selection(self, cars):
        cars.sort(key = self.sort_by_score, reverse=True)
        print ([car.score for car in cars])
        cars_upd = deepcopy(cars[:max_cars])
        '''
        print (len(cars))
        
        i = 0
        while i <= len(cars)-2:
            if cars[i].score < cars[i+1].score:
                print(cars[i].score)
                cars.pop(i)
            else:
                print(cars[i+1].score)
                cars.pop(i+1)
            i += 1
            print (len(cars))
            print ("i", i)
        #print ("end",len(cars))  
        if len(cars)>max_cars:
            self.selection(cars)
        
        #print ("in selection")
        #self.check_for_repeats(cars)
        #print ([car.score for car in cars])
        print ([car.score for car in cars])
        '''
        return cars_upd
    
    def check_for_repeats(self, cars):
        i=0
        j=0
        while i<len(cars)-1:
            while j<len(cars)-1:
                if all(cars[i].gen == cars[j].gen) and cars[i] != cars[j]:
                    print ("we are here")
                    cars.pop(j)
                    j -= 1
                j += 1
            i += 1   
        return cars
        
    
    
