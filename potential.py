import torch
import sklearn
import sklearn.datasets
import numpy as np

batch_size = 256
epsilon = 0.1

moon_data_pack = sklearn.datasets.make_moons()
data = moon_data_pack[0]

data = np.array(data)
data = torch.from_numpy(data).float()
data.requires_grad_(False)

class PotentialNet(torch.nn.Module):
    def __init__(self,
                 in_dim = 2,
                 hidden_dim = 6,
                 out_dim = 1):
        super(PotentialNet, self).__init__()

        self.fc = torch.nn.Sequential(
            torch.nn.Linear(in_dim,hidden_dim),
            torch.nn.ReLU(),
            torch.nn.Linear(hidden_dim,out_dim),
        )

    def forward(self,x):
        return self.fc(x)

def get_dist(x1,x2):
    sum = 0
    for i in range(len(x1)):
        sum += (x1[i] - x2[i]) ** 2
    return np.sqrt(sum)

def get_func_term(v,x,y):
    batch_x = x.shape[0]
    batch_y = y.shape[0]

    sum = 0
    for i in range(batch_x):
        cur = 0
        for j in range(batch_y):
            dist = get_dist(x[i],y[j])
            cur += torch.exp((v[j] - dist)/epsilon)
        sum = sum - epsilon * torch.log(cur)
    return sum/batch_x

potential_net = PotentialNet()
optimizer = torch.optim.SGD(potential_net.parameters(), 
                            lr = 0.01, 
                            momentum=0.9)

for epoch in range(10000000000):
    optimizer.zero_grad()

    y = np.random.multivariate_normal((0,0), 
                                      np.array([[1, 0], [0, 1]]), 
                                      (batch_size,))
    y = torch.from_numpy(y).float()
    y.requires_grad_(False)

    v = potential_net(y)

    loss_first_term = get_func_term(v,data,y)
    loss_second_term = torch.mean(v)
    loss = -loss_first_term - loss_second_term + epsilon
    
    loss.backward()
    if epoch % 1 == 0:
        print(epoch, loss)

    optimizer.step()
