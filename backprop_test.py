from numpy import *
import matplotlib.pyplot as plt
from random import shuffle


NEURONS = 20
LAMBD = 0.2


def evaluate(inpt, Theta_1, Theta_2):
        #Theta_1 = self.get_theta1()
        #Theta_2 = self.get_theta2()
        
#         print ("input",inpt)
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
#     J = 1/m * sum(sum(a)) + lambda/(2*m)*(sum(sum(Theta1(:,2:end) .^2))+sum(sum(Theta2(:,2:end) .^2)));
    return sum(sum(power((h-Y),2)))/(2*m) + LAMBD/(2*m)*sum_theta
# return 1./m *sum(sum(a))


def gradinet_check(X_train, Theta_1, Theta_2):
    eps = 0.0001
    
    grad_1 = zeros(shape(Theta_1))
    
    for i in range(shape(Theta_1)[0]):
        for j in range(shape(Theta_1)[1]):
            temp_theta_1 = copy(Theta_1)
            temp_theta_1[i][j] += eps
#             car.set_theta1(temp_theta_1)
            J_plus_eps = cost(X_train, Y_train, temp_theta_1, Theta_2)
            temp_theta_1[i][j] -= 2*eps
#             car.set_theta1(temp_theta_1)
#             evaluation,z_1,z_2 = evaluate(X_train, temp_theta_1, Theta_2)
            J_minus_eps = cost(X_train, Y_train, temp_theta_1, Theta_2)
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
            J_plus_eps = cost(X_train, Y_train, Theta_1, temp_theta_2)
            temp_theta_2[i][j] -= 2*eps
#             car.set_theta2(temp_theta_2)
#             evaluation,z_1,z_2 = car.evaluate(X_train)
            J_minus_eps = cost(X_train, Y_train, Theta_1, temp_theta_2)
            grad_2[i][j] = (J_plus_eps - J_minus_eps)/(2*eps)
            print ("jplus", J_plus_eps)
            print ("jminus", J_minus_eps)
            print ((J_plus_eps - J_minus_eps)/(2*eps))
#     car.set_theta2(Theta_2)
    
    
    return grad_1, grad_2

def get_data():
    Theta_1 = (random.rand(14*NEURONS) - 0.5).reshape(14, NEURONS) *  1
    Theta_2 = (random.rand((NEURONS+1)*2) - 0.5).reshape(NEURONS+1, 2) * 1
    
    data = load("training_data_c" + '.npy', encoding="latin1")
    print (shape(data))
#     random.shuffle(data)
    print (shape(data))
    X = data[0][0]
    X = list(X)
#     random.shuffle(X)
    Y = data[1][0]
    Y = list(Y)
    random.shuffle(Y)

#     Y[:][Y<0.5] = 0.5
    train_test_split = int(0.7*shape(X)[0])
    
    X_train = X[:train_test_split]
#     X_train = ones(shape(X_train))
    X_test= X[train_test_split:]
    
    Y_train = Y[:train_test_split]
    Y_test= Y[train_test_split:]
    
    evaluation,z_1, z_2, z_3, a_1, a_2 = evaluate(X_train, Theta_1, Theta_2)
    return evaluation, Theta_1, Theta_2, X_train, X_test, Y_train, Y_test



def sigmoid(a):
    return 2./(1+exp(-a))-1 #[-1;1]

def relu(a):
    a[a<0] = 0
    return a

def sigmoid_gradient(a):
    return 2./(1+exp(-a))*(1-1./(1+exp(-a)))

def relu_gradient(a):
    a[a > 0] = 1
    a[a <= 0] = 0
    return a

def gradiend_descent(X_train, Y_train, Theta_1, Theta_2, alpha, epochs = 100, test = False, X_test = NaN, Y_test = NaN):
    m = shape(X_train)[0]
    J = []
    J_test = []
    for i in range(epochs):
        D1, D2 = train_brain(X_train, Y_train, Theta_1, Theta_2)
        Theta_1 = Theta_1 - alpha*D1 - LAMBD/(2*m)
        Theta_2 = Theta_2 - alpha*D2 - LAMBD/(2*m)
        J.append(cost(X_train, Y_train, Theta_1, Theta_2))
        if test == True:
            J_test.append(cost(X_test, Y_test, Theta_1, Theta_2))
             
    print (Theta_1)
    if test == True:
        return J, J_test  
    return J
    
def get_gradient(X_train, Y_train, Theta_1, Theta_2):
    evaluation,z_1,z_2,z_3, a_1, a_2 = evaluate(X_train, Theta_1, Theta_2)
    m = shape(evaluation)[0]

    delta_3 = (evaluation - Y_train)*sigmoid_gradient(z_3)
#         print ("delta 3", shape(delta_3))
#         print ("Thet 2.T", shape(Theta_2.T))
#         print ("D2 shape", shape(dot(a_2.T,delta_3)))
# #         D2 =  1./m*(dot(a_2.T,delta_3) + lambd*Theta_2)
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


def train_brain(X_train, Y_train, Theta_1, Theta_2, alpha = 1, epochs = 200,  X_test = NaN, Y_test = NaN):
    m = shape(evaluation)[0]
    J = []
    J_test = []
    for i in range(epochs):
        D1, D2 = get_gradient(X_train, Y_train, Theta_1, Theta_2)
        Theta_1 = Theta_1 - alpha*D1 - LAMBD/(2*m)
        Theta_2 = Theta_2 - alpha*D2 - LAMBD/(2*m)
        J.append(cost(X_train, Y_train, Theta_1, Theta_2))
        J_test.append(cost(X_test, Y_test, Theta_1, Theta_2))
            
    print (Theta_1)
    return J, J_test  
    return J
    
evaluation, Theta_1, Theta_2, X_train, X_test, Y_train, Y_test = get_data()    
# G1, G2 = gradinet_check(X_train, Theta_1, Theta_2)
# D1, D2 = train_brain(X_train, Y_train, Theta_1, Theta_2)

alphas = [0.06*power(i,2) for i in range(20)]

# J = array([gradiend_descent(X_train, Y_train, Theta_1, Theta_2, alpha, 200) for alpha in alphas])

# best_alpha = argmin(J[:,190])
print ()

# J = array([gradiend_descent(X_train, Y_train, Theta_1, Theta_2, alpha, 200) for alpha in alphas])
Res = []

NEURONS = 25
Theta_1 = (random.rand(14*NEURONS) - 0.5).reshape(14, NEURONS) *  1
Theta_2 = (random.rand((NEURONS+1)*2) - 0.5).reshape(NEURONS+1, 2) * 1
# J, J_test = gradiend_descent(X_train, Y_train, Theta_1, Theta_2, 0.4, 200, True, X_test, Y_test)
# Res.append(J[len(J_test)-1]/J_test[len(J_test)-1])
# print ("test/train error", J[len(J_test)-1]/J_test[len(J_test)-1])
# print (J_test)
J, J_test = train_brain(X_train, Y_train, Theta_1, Theta_2, 1, 100, X_test, Y_test)
plt.plot(J_test)
plt.plot(J)
# plt.plot(J_test)
plt.ylabel('some numbers')
plt.show()
# print ("test/train error", J[len(J_test)-1]/J_test[len(J_test)-1])


# print ("theta_1 grad", D1, G1)
# print ("theta_2 grad", D2, G2)
