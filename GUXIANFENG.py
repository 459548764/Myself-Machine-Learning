import numpy as np
import torch

import ot

n_sample = 10000
epsilon = 0.1

source_data = np.random.random([n_sample,2]) * 2 - 1

target_data = np.array([[0.4, 0.7],
                   [-0.5, 0.5],
                   [-0.8, -0.2],
                   [0.6, -0.8]])

source_weights = np.ones(n_sample, ) / n_sample
target_weights = np.array([0.3, 0.2, 0.1, 0.4])

M = ot.dist(source_data, target_data)

source_weights = torch.from_numpy(source_weights).float()
target_weights = torch.from_numpy(target_weights).float()

source_data = torch.from_numpy(source_data).float()
target_data = torch.from_numpy(target_data).float()
M = torch.from_numpy(M).float() 

g = 0 * torch.rand([4]).float()
g = torch.tensor(g,requires_grad=True)


for epoch in range(0,10):
    
    t_sum = 0
    for i in range(n_sample):
        s = 0 
        
        idx = -1
        mymax = -10000
        for j in range(4):
            cur = g[j] - M[i][j]
            if cur > mymax:
                mymax = cur
                idx = j
        t_sum += source_weights[i] * (g[idx] - M[i][idx])

    g_sum = 0
    for j in range(4):
        g_sum += target_weights[j] * (g[j])
                         
    loss = t_sum - g_sum
    loss.backward()
    
    if epoch % 1 == 0:
        print(epoch, loss, g)
        
    g.data.sub_(1 * g.grad.data)
    g.grad.data.zero_()
    
    final_g = g.detach().numpy()

target_datax = np.array([[0.4, 0.7],
                   [-0.5, 0.5],
                   [-0.8, -0.2],
                   [0.6, -0.8]])

x = np.linspace(-1, 1, 20)
y = np.linspace(-1, 1, 20)

result = np.zeros([100, 100])

for i in range(100):
    for j in range(100):
        test = np.zeros([1, 2])
        test[0][0] = -1 + 2/100 * j
        test[0][1] = 1 - 2/100 * i
        m = ot.dist(test, target_datax)
        print(test, m)
        result[i][j] = np.argmax(final_g - m)
        
import matplotlib.pyplot as plt

plt.imshow(result)
plt.colorbar()
plt.savefig('2ss.pdf')
