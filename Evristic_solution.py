from numpy import *
from Car import Car, sensors_nb, NEURONS_NB
from copy import deepcopy#, copy
X_points = 3
to_mutation = 0.4
max_cars = 3



random.seed(1234567890)

class Evristic():
    
    def __init__(self):
        self.iter = 0
        self.update_lambda()
    
    def give_next_generation(self, cars):
        new_cars = self.mutation(cars)#[:int(to_mutation * len(cars))])
        print ("after mutation")
        self.check_for_repeats(cars + new_cars)
        print ("len after mutation", len(new_cars))
        new_cars += self.crossbreeding(cars)#[int(to_mutation * len(cars)):])
        print ("len after crossbreeding", len(new_cars))
        print (len(cars + new_cars))
        print ("after crossbreeding")
        cars = self.check_for_repeats(cars+new_cars)
        #print (len(cars+new_cars))
        return cars
        #[cars.append(new_car) for new_car in new_cars]
        #self.check_for_repeats(cars)
        #return cars
    
    def update_lambda(self):
        if self.iter < 360:
            self.iter += 1
        self.lmbd = exp(-300.0/(400.0-self.iter))
        
    
    def mutation(self, old_cars):
        self.update_lambda()
        new_cars=[]
        for old_car in old_cars:
            new_cars.append(Car(old_car.gen.copy()))
                  
        for car in new_cars:
            a = array(random.uniform(-self.lmbd, self.lmbd, len(car.gen)))
            car.gen += multiply(car.gen, a)
                    
        print ("inside mutation")  
        print (len(new_cars+old_cars))
        self.check_for_repeats(new_cars+old_cars)
        print ("len after clean", len(new_cars+old_cars))
        return new_cars
            
    
    def crossbreeding(self, old_cars):
        new_cars = []
        for old_car in old_cars:
            new_cars.append(Car(old_car.gen.copy()))
        if len(new_cars) % 2 == 1:
            new_cars.pop()
        for i in range(len(new_cars)):
            if i % 2 == 1:
                continue
            for iter in range(X_points):
                point = random.randint(1, len(new_cars[i].gen) - 2)
                print ("crossbreeding points", point, i)
                print (len(new_cars[i+1].gen))
                
                #temp = copy(new_cars[i+1].gen[:point])
                #print (new_cars[i].gen[:3])
                #new_cars[i+1].gen[:point] = copy(new_cars[i].gen[:point])
                #new_cars[i].gen[:point] = copy(temp)
                new_cars[i].gen[:point], new_cars[i+1].gen[:point] = new_cars[i+1].gen[:point].copy(), new_cars[i].gen[:point].copy()
                #new_cars[i].gen[:point], new_cars[i+1].gen[:point] = new_cars[i+1].gen[:point], new_cars[i].gen[:point]
                print ("log test inside cross", all(new_cars[i].gen == old_cars[i+1].gen))
        print ("inside crossbreeding")
        self.check_for_repeats(old_cars + new_cars)
        #for car in new_cars:
        #    print (car.gen[:3])
        return new_cars
                
#     def shuffle(self,cars):
#         for i in range(len(cars)-1):
#             j = random.randint(i, len(cars)-1)
#             tmp = deepcopy(cars[i])
#             cars[i] = deepcopy(cars[j])
#             cars[j] = deepcopy(tmp)
#         return cars
    
    def sort_by_score(self,car):
        return car.score
    
    def selection(self, cars):
        cars.sort(key = self.sort_by_score, reverse=True)
        print ([car.score for car in cars])
        #print ([car.score for car in cars])
        cars_upd = deepcopy(cars[:max_cars])
        print ("inside selection")
        self.check_for_repeats(cars_upd)
        print ([car.score for car in cars_upd])
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
        while i<len(cars):
            while j<len(cars):
                #print(all(cars[i].gen == cars[j].gen))
                if all(cars[i].gen == cars[j].gen) and i != j:
                    print ("i and J", i, j)
                    #print (cars[i].gen)
                    print ("!!WE ARE HERE!!")
                    cars.pop(j)
                    j -= 1
                j += 1
            j = 0
            i += 1
        print ("length of list after repeats", len(cars))
        return cars
        
    
    
