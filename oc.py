
import torch

class Net(torch.nn.Module):
    def __init__(self,
                 in_dim = 2,
                 hidden_dim = 10,
                 out_dim = 1):
        super(Net, self).__init__()
        self.fc = torch.nn.Sequential(
            torch.nn.Linear(in_dim, hidden_dim),
            torch.nn.ReLU(),
            torch.nn.Linear(hidden_dim, out_dim),
            torch.nn.ReLU(),
        )


    def forward(self,x,t):
        input = torch.cat([x,t])
        result = self.fc(input)
        return result

    def simulation(self,x,t,time_step):
        x = torch.tensor([x]).float()
        t = torch.tensor([t]).float()
        x_new = x + self.forward(x,t) * time_step
        return x_new

    def process(self,x,t,time_duration):
        energy = 0
        for i in range(time_duration):
            self.simulation(x,t)


time_step = 1
time_duration = 10

initial_state = 0
initial_time = 0

destination = 3

net = Net()
optimizer = torch.optim.Adam(net.parameters(), lr=0.01)

def simulation(x,t,time_duration,time_step):
    energy_sum = 0
    v = []

    for i in range(time_duration):
        x = torch.tensor([x]).float()
        t = torch.tensor([t]).float()

        get_v = net(x,t)
        energy_sum += get_v ** 2

        x_new = x + get_v * time_step
        t_new = t + time_step

        x = x_new
        t = t_new
        v.append(get_v)

    return x,energy_sum/time_duration,v


for epoch in range(10000000):
    optimizer.zero_grad()

    x, energy_sum, v = simulation(initial_state,
                                  initial_time,
                                  time_duration,
                                  time_step)

    loss_dis = (x - destination) ** 2
    loss_ent = energy_sum

    loss = loss_dis + 0.0001 * loss_ent
    if epoch % 1000 == 0:
        print(loss, loss_dis, loss_ent)
        # print(x)
        # print(v)

    loss.backward()

    optimizer.step()
