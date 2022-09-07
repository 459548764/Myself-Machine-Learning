def loss(pi):
    # pi 4*1
    cost = torch.Tensor([[1, 3, 3, 1]])  # 1 * 4
    
    omega_1 = torch.tensor([[1., 1, 0, 0]])
    omega_2 = torch.tensor([[0., 0, 1, 1]])

    phi_1 = torch.tensor([[1., 0, 1, 0]])
    phi_2 = torch.tensor([[0., 1, 0, 1]])
    
    mat = torch.tensor([[1., 1, 0, 0], [0., 0, 1, 1], [1., 0, 1, 0], [0., 1, 0, 1]]) # 4 * 4
    
    res = torch.tensor([[1., 1, 1, 1]])
    
#     y = cost @ pi + torch.sum((mat @ pi - res) ** 2)
    
    y = cost @ pi + (omega_1@pi-1)**2 + (omega_2@pi-1)**2 + (phi_1@pi-1)**2 + (phi_2@pi-1)**2
    return y

pi = Variable(torch.Tensor([[0],[1],[1],[0]]), requires_grad=True)

for _ in range(10):
    grad_pi = torch.autograd.grad(loss(pi), pi, create_graph=True)

    step = torch.linalg.inv(grad_pi[0] @ grad_pi[0].T + 0.1 * torch.eye(4)) @ grad_pi[0] @ loss(pi)

    pi = pi - step

    pi = torch.clamp(pi, min = 0)

    print(pi)
