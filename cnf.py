import torch
from module import ODE_FUNC

import time

class CNF():
    def __init__(self,
                 in_dim,
                 hidden_dim,
                 out_dim):

        self.ode_func = ODE_FUNC(in_dim,hidden_dim,out_dim)

    def get_simulation(self,x0,t0,step,T):
        x = x0
        t = t0
        d_trace = 0

        for i in range(T):
            f = self.ode_func(x,t)
            d_trace += self.ode_func.get_trace()

            x = x + f * step
            t = t + step

        return x,d_trace


in_dim = 3
hidden_dim = 6
out_dim = 3

batch_size = 1
step = 0.1
T = 10

cnf = CNF(in_dim = 3, hidden_dim = 6, out_dim = 3)
optimizer = torch.optim.SGD(cnf.ode_func.parameters(), lr = 0.0001, momentum=0.9)

for epoch in range(10000):
    optimizer.zero_grad()

    x = torch.ones(batch_size,in_dim,requires_grad = True)
    t = torch.zeros(batch_size,1,requires_grad = True)

    x_final, d_trace = cnf.get_simulation(x,t,step,T)

    loss_e = 0.5 * torch.mean(x_final ** 2)
    loss = loss_e - d_trace
    # loss = torch.clamp(loss_e - d_trace, min = 0)

    loss.backward()
    print(loss,x_final)
    time.sleep(1)
    optimizer.step()
