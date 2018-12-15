from numpy import *
from Car import Car, sensors_nb, NEURONS_NB
from copy import deepcopy#, copy
X_points = 3
to_mutation = 0.4
max_cars = 10


iter = 0
lmbd = 0.1#exp(-2000.0/(400.0-iter))
    
def give_next_generation(cars):
    new_cars = mutation(cars)#[:int(to_mutation * len(cars))])
    print ("after mutation")
    check_for_repeats(cars + new_cars)
    new_cars += crossbreeding(cars)#[int(to_mutation * len(cars)):])
    print ("after crossbreeding")
    cars = check_for_repeats(cars+new_cars)
        #print (len(cars+new_cars))
    return cars
        #[cars.append(new_car) for new_car in new_cars]
        #check_for_repeats(cars)
        #return cars
    
def update_lambda(iter):
    if iter < 360:
        iter += 1
    lmbd = exp(-300.0/(200.0-iter))
    lmbd = 0.1
        
    
def mutation(old_cars):
    update_lambda(iter)
    new_cars=[]
    for old_car in old_cars:
        new_cars.append(Car(copy(old_car.gen)))
              
    for car in new_cars:
        a = array(random.uniform(-lmbd, lmbd, len(car.gen)))
        car.gen += multiply(car.gen, a)
                
    check_for_repeats(new_cars+old_cars)
    return new_cars
        

def crossbreeding(old_cars):
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
            #temp = copy(new_cars[i+1].gen[:point])
            #print (new_cars[i].gen[:3])
            #new_cars[i+1].gen[:point] = copy(new_cars[i].gen[:point])
            #new_cars[i].gen[:point] = copy(temp)
            new_cars[i].gen[:point], new_cars[i+1].gen[:point] = new_cars[i+1].gen[:point].copy(), new_cars[i].gen[:point].copy()
            #new_cars[i].gen[:point], new_cars[i+1].gen[:point] = new_cars[i+1].gen[:point], new_cars[i].gen[:point]
    check_for_repeats(old_cars + new_cars)
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

def sort_by_score(car):
    return car.score

def selection(cars):
#     cars.sort(key = sort_by_score, reverse=True)
#     print ([car.score for car in cars])
#     #print ([car.score for car in cars])
#     cars = deepcopy(cars[:max_cars])
#     for i in range(len(cars)):
#         if i == 0:
#             cars[0].is_leader = True
#         else:
#             cars[i].is_leader = False
#     
#     print ("inside selection")
#     check_for_repeats(cars)
#     print (len(cars))
# #     
    i = 0
    cars.sort(key = sort_by_score, reverse=True)
    while i <= len(cars)-2:
        if cars[i].score < cars[i+1].score:
#             print(cars[i].score)
            cars.pop(i)
        else:
            print(cars[i+1].score)
            cars.pop(i+1)
        i += 1
#         print (len(cars))
#         print ("i", i)
    #print ("end",len(cars))  
    if len(cars)>max_cars:
        selection(cars)
     
    #print ("in selection")
    #check_for_repeats(cars)
    #print ([car.score for car in cars])
#     print ([car.score for car in cars])
    check_for_repeats(cars)
    return cars

def check_for_repeats(cars):
    i=0
    j=0
    while i<len(cars):
        while j<len(cars):
            #print(all(cars[i].gen == cars[j].gen))
            if all(cars[i].gen == cars[j].gen) and i != j:
                print (i)
                print ("!!WE ARE HERE!!")
                cars.pop(j)
                j -= 1
            j += 1
        j = 0
        i += 1
    return cars
    
    
    
