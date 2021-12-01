
import torch
from torch.nn.modules.activation import Tanh
from torch.nn.modules.normalization import LayerNorm

class Flow_Net(torch.nn.Module):
    def __init__(self,
                 dim):
        super(Flow_Net, self).__init__()
        self.w = torch.rand(dim, dim).float()
        self.b = torch.rand(dim).float()
        self.u = torch.rand(dim, dim).float()

        self.w.requires_grad_(True)
        self.b.requires_grad_(True)
        self.u.requires_grad_(True)

        self.diff_f = lambda x: 1 - torch.tanh(x)**2
        self.act_f = lambda x: torch.tanh(x)

    def forward(self,x):
        '''
        z.shape := [batch, dim]
        det_jacobian.shape := [batch]
        '''
        v = x @ self.w + self.b
        z = x + self.act_f(v) @ self.u

        psi = self.diff_f(v) @ self.w
        det_jacobian = torch.abs(1 + torch.sum(psi @ self.u, dim=-1))
        return z, det_jacobian
        
    
dim = 2

flow_net = Flow_Net(dim)

x = torch.rand(128,dim)

flow_net(x)
