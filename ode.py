import torch 

class ODE_FUNC(torch.nn.Module):
    def __init__(self,
                 in_dim,
                 hidden_dim,
                 out_dim):
        super(ODE_FUNC, self).__init__()

        self.in_dim = in_dim
        self.hidden_dim = hidden_dim
        self.out_dim = out_dim

        self.fx = torch.nn.Sequential(
            torch.nn.Linear(self.in_dim, self.hidden_dim),
            torch.nn.ReLU(),
            torch.nn.Linear(self.hidden_dim, self.out_dim),
        )

        self.ft = torch.nn.Sequential(
            torch.nn.Linear(1, self.hidden_dim),
            torch.nn.ReLU(),
            torch.nn.Linear(self.hidden_dim, self.out_dim),
        )

    def forward(self,x,t):
        self.x = x
        self.t = t
        self.out = self.fx(self.x) + self.ft(self.t)
        return self.out

    def get_trace(self):
        result = 0
        for i in range(self.out_dim):
            # 计算trace。注意的是，这里是取出第i个变量下第i位的数据并求和得到的结果。
            result += torch.autograd.grad(self.out[:,i].sum(), 
                                          self.x, 
                                          retain_graph=True, 
                                          create_graph=True)[0].contiguous()[:,i].contiguous()
        return result

in_dim = 3
hidden_dim = 6
out_dim = 3

batch_size = 1

x = torch.ones(batch_size,in_dim,requires_grad = True)
t = torch.ones(batch_size,1,requires_grad = True)

ode_func = ODE_FUNC(in_dim,hidden_dim,out_dim)

f = ode_func(x,t)

print(ode_func.get_trace())

x = x + f * 1

f = ode_func(x,t)

print(ode_func.get_trace())
