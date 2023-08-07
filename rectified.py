import torch
import numpy as np
import torch.nn as nn
import ot

class MLPDiffusion(nn.Module):
    def __init__(self, n_steps, num_units=128):
        super(MLPDiffusion, self).__init__()

        self.linears = nn.ModuleList(
            [
                nn.Linear(2, num_units),
                nn.ReLU(),
                nn.Linear(num_units, num_units),
                nn.ReLU(),
                nn.Linear(num_units, num_units),
                nn.ReLU(),
                nn.Linear(num_units, 2),
            ]
        )
        self.step_embeddings = nn.ModuleList(
            [
                nn.Embedding(n_steps, num_units),
                nn.Embedding(n_steps, num_units),
                nn.Embedding(n_steps, num_units),
            ]
        )

    def forward(self, x, t):
        for idx, embedding_layer in enumerate(self.step_embeddings):
            t_embedding = embedding_layer(t)
            x = self.linears[2 * idx](x)
            
            x += t_embedding
            x = self.linears[2 * idx + 1](x)

        x = self.linears[-1](x)

        return x
    
num_steps = 100
model = MLPDiffusion(num_steps)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

n = 500  # nb samples

mu_s = np.array([0, 0])
cov_s = np.array([[1, 0], [0, 1]])

mu_t = np.array([4, 4])
cov_t = np.array([[1, -.8], [-.8, 1]])

src_data = ot.datasets.make_2D_samples_gauss(n, mu_s, cov_s)
trg_data = ot.datasets.make_2D_samples_gauss(n, mu_t, cov_t)

a, b = np.ones((n,)) / n, np.ones((n,)) / n  # uniform distribution on samples


step = 100
batch_size = 120

for epoch in range(100):
    src_index = np.random.choice(n, size=batch_size, replace=False)
    trg_index = np.random.choice(n, size=batch_size, replace=False)

    batch_src_data = src_data[src_index]
    batch_trg_data = trg_data[trg_index]

    # src_weight, trg_weight = np.ones((batch_size,)) / batch_size, np.ones((batch_size,)) / batch_size
    # cost_matrix = ot.dist(batch_src_data, batch_trg_data)
    # pi_matrix = ot.emd(src_weight, trg_weight, cost_matrix)
    # map_data = batch_size * pi_matrix @ batch_trg_data

    map_data = batch_trg_data

    loss = 0
    for i in range(num_steps):
        direction = torch.from_numpy((map_data - batch_src_data) / num_steps)
        move_position =  i/num_steps * map_data + (1 - i/num_steps) * batch_src_data
        pred_dir = model(torch.from_numpy(move_position).float(), torch.tensor(i))
        loss += torch.mean((pred_dir - direction) ** 2)
    optimizer.zero_grad()
    print(epoch, loss)
    loss.backward()
    optimizer.step()

print('-----')

import copy
# model = model.to('cpu')
# 如果模型当前在GPU上而你对此不放心的话
model_copy = copy.deepcopy(model)

for epoch in range(100):
    src_index = np.random.choice(n, size=batch_size, replace=False)
    trg_index = np.random.choice(n, size=batch_size, replace=False)

    batch_src_data = src_data[src_index]
    batch_trg_data = trg_data[trg_index]

    map_data = batch_src_data
    for i in range(num_steps):
        map_data += model_copy(torch.from_numpy(map_data).float(), torch.tensor(0)).detach().numpy()

    optimizer.zero_grad()
    loss = 0
    for i in range(num_steps):
        direction = torch.from_numpy((map_data - batch_src_data) / num_steps)
        move_position =  i/num_steps * map_data + (1 - i/num_steps) * batch_src_data
        pred_dir = model(torch.from_numpy(move_position).float(), torch.tensor(i))
        loss += torch.mean((pred_dir - direction) ** 2)
    optimizer.zero_grad()
    print(epoch, loss)
    loss.backward()
    optimizer.step()

print('-----')

import copy
# model = model.to('cpu')
# 如果模型当前在GPU上而你对此不放心的话
model_copy = copy.deepcopy(model)

for epoch in range(100):
    src_index = np.random.choice(n, size=batch_size, replace=False)
    trg_index = np.random.choice(n, size=batch_size, replace=False)

    batch_src_data = src_data[src_index]
    batch_trg_data = trg_data[trg_index]

    map_data = batch_src_data
    for i in range(num_steps):
        map_data += model_copy(torch.from_numpy(map_data).float(), torch.tensor(0)).detach().numpy()
    optimizer.zero_grad()

    loss = 0
    for i in range(num_steps):
        direction = torch.from_numpy((map_data - batch_src_data) / num_steps)
        move_position =  i/num_steps * map_data + (1 - i/num_steps) * batch_src_data
        pred_dir = model(torch.from_numpy(move_position).float(), torch.tensor(i))
        loss += torch.mean((pred_dir - direction) ** 2)
    optimizer.zero_grad()
    print(epoch, loss)
    loss.backward()
    optimizer.step()

src_index = np.random.choice(n, size=10, replace=False) 
batch_src_data = src_data[src_index]

pred_dir = model(torch.from_numpy(batch_src_data).float(), torch.tensor(0))
print(torch.from_numpy(batch_src_data) + pred_dir * num_steps)
