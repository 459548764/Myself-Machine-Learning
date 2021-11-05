
import torch
import numpy as np
from torch.autograd import Variable

positive_data = np.array([[0,0],
                          [1,0],
                          [2,0],
                          [3,0],
                          [4,0]])

unlabeled_data = np.array([[0,1],
                           [1,1],
                           [2,10],
                           [3,10],
                           [4,10]])


a = np.array([1/5,1/5,1/5,1/5,1/5])
b = np.array([1,1,0.1,0.1,0.1])


def get_dist(x1,x2):
    sum = 0
    for i in range(len(x1)):
        sum += (x1[i] - x2[i]) ** 2
    return np.sqrt(sum)

cost = [[0 for _ in range(5)] for _ in range(5)]

for i in range(5):
    for j in range(5):
        cost[i][j] = get_dist(positive_data[i],unlabeled_data[j])
cost = np.array(cost)


def get_KL(list1,list2):
    kl_sum = 0

    for i in range(list1.shape[0]):
        kl_sum += list1[i] * torch.log(list1[i] / (list2[i] + 0.001))
        kl_sum -= list1[i]
        kl_sum += list2[i]
    return kl_sum

def get_Ent(mat_pi):
    row = mat_pi.shape[0]
    col = mat_pi.shape[1]

    ent_sum = 0
    for i in range(row):
        for j in range(col):
            ent_sum += mat_pi[i][j] * torch.log(mat_pi[i][j] + 0.001)

    return ent_sum

def get_Move(mat_cost,mat_pi):
    row = mat_pi.shape[0]
    col = mat_pi.shape[1]
    transport_mat = mat_cost * mat_pi
    
    move_sum = 0
    for i in range(row):
        for j in range(col):
            move_sum += transport_mat[i][j] 

    return transport_mat, move_sum

positive_data = torch.from_numpy(positive_data).double()
unlabeled_data = torch.from_numpy(unlabeled_data).double()

weight_a = torch.from_numpy(a).double()
weight_b = torch.from_numpy(b).double()

cost = torch.from_numpy(cost).double()

num_pos = positive_data.shape[0]
num_unl = unlabeled_data.shape[0]

pi = torch.rand([num_pos,num_unl]).double()
pi = torch.tensor(pi,requires_grad=True)

tau = 1
epsilon = 1
lr = 0.0000001

for epoch in range(0,1000000000000):

    mat_trans, loss_emd = get_Move(cost, pi)

    sum_col = torch.sum(mat_trans,dim=1)
    sum_row = torch.sum(mat_trans,dim=0)

    loss_kl_col = get_KL(sum_col, weight_b)
    loss_kl_row = get_KL(sum_row, weight_a)
    loss_ent = get_Ent(pi)
    loss = loss_emd + epsilon * loss_ent + tau * (loss_kl_col + loss_kl_row)

    loss.backward()
    if epoch % 1000 == 0:
        print(epoch, loss)
        print(pi)

    pi.data.sub_(lr * pi.grad.data)
    pi.grad.data.zero_()
