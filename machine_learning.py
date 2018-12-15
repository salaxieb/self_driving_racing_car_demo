from numpy import *
from Car import Car, evaluate
lambd = 0
def cost(inpt, Y, Theta_1, Theta_2, lambd):
    
    h, z_1, z_2, a_1, a_2 = evaluate(inpt, Theta_1, Theta_2)
    
    m = shape(h)[0]
    sum_theta = 0
    sum_theta += sum(sum(dot(Theta_1[1:,:].T,Theta_1[1:,:]))) #droppping bias
    sum_theta += sum(sum(dot(Theta_2[1:,:].T,Theta_2[1:,:])))
    return sum(sum(power((h-Y),2)))/m + lambd/(2*m)*sum_theta     

def gradinet_check(X_train, Theta_1, Theta_2):
    eps = 0.00001
    
    grad_1 = zeros(shape(Theta_1))
    
    for i in range(shape(Theta_1)[0]):
        for j in range(shape(Theta_1)[1]):
            temp_theta_1 = copy(Theta_1)
            temp_theta_1[i][j] += eps
#             car.set_theta1(temp_theta_1)
            J_plus_eps = cost(X_train, Y_train, temp_theta_1, Theta_2, lambd)
            temp_theta_1[i][j] -= 2*eps
#             car.set_theta1(temp_theta_1)
#             evaluation,z_1,z_2 = evaluate(X_train, temp_theta_1, Theta_2)
            J_minus_eps = cost(X_train, Y_train, temp_theta_1, Theta_2, lambd)
            grad_1[i][j] = (J_plus_eps - J_minus_eps)/(2*eps)
            print ("jplus", J_plus_eps)
            print ("jminus", J_minus_eps)
            print ((J_plus_eps - J_minus_eps)/(2*eps))
            print ("gradient_1", grad_1)
            
#     car.set_theta1(Theta_1)
            
    grad_2 = zeros(shape(Theta_2))
            
    for i in range(shape(Theta_2)[0]):
        for j in range(shape(Theta_2)[1]):
            temp_theta_2 = copy(Theta_2)
            temp_theta_2[i][j] += eps
#             car.set_theta2(temp_theta_2)
#             evaluation,z_1,z_2 = car.evaluate(X_train)
            J_plus_eps = cost(X_train, Y_train, Theta_1, temp_theta_2, lambd)
            temp_theta_2[i][j] -= 2*eps
#             car.set_theta2(temp_theta_2)
#             evaluation,z_1,z_2 = car.evaluate(X_train)
            J_minus_eps = cost(X_train, Y_train, Theta_1, temp_theta_2, lambd)
            grad_2[i][j] = (J_plus_eps - J_minus_eps)/(2*eps)
            print ("jplus", J_plus_eps)
            print ("jminus", J_minus_eps)
            print ((J_plus_eps - J_minus_eps)/(2*eps))
#     car.set_theta2(Theta_2)
    
    
    return grad_1, grad_2
    
    

def get_data(car):
    Theta_1 = car.get_theta1()
    Theta_2 = car.get_theta2()
    data = load("training_data_c" + '.npy')

    X = list(data[0][0])
    Y = list(data[1][0])
    train_test_split = int(0.02*shape(X)[0])
    
    X_train = X[:train_test_split]
#     X_train = ones(shape(X_train))
    X_test= X[train_test_split:]
    
    Y_train = Y[:train_test_split]
    Y_test= Y[train_test_split:]
    
    evaluation,z_1,z_2, a_1, a_2 = evaluate(X_train, Theta_1, Theta_2)
    return evaluation, Theta_1, Theta_2, X_train, X_test, Y_train, Y_test

car = Car()
evaluation, Theta_1, Theta_2, X_train, X_test, Y_train, Y_test = get_data(car)

J = cost(X_train, Y_train, Theta_1, Theta_2, lambd)

print ("j",J)

data = load("training_data_c" + '.npy')

G1, G2 = gradinet_check(X_train, car.get_theta1(), car.get_theta2())
D1, D2 = car.train_brain(X_train, Y_train)
print ("theta_1 grad", D1, G1)
print ("theta_2 grad", D2, G2)
    
    
    