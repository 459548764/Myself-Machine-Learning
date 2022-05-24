import numpy as np
import ot

class OT_ADMM():
    def __init__(self):
        pass
    
    def load_data(self, src_data, trg_data, src_weight, trg_weight, rho):
        self.src_data = src_data
        self.trg_data = trg_data
        self.rho = rho
        
        self.src_samples = self.src_data.shape[0]
        self.trg_samples = self.trg_data.shape[0]
        
        self.cost = ot.dist(self.src_data, self.trg_data)
        self.cost = np.reshape(self.cost, -1)[:,np.newaxis]
        
        self.weight = np.concatenate((src_weight, trg_weight), axis = 0)
        self.gamma = src_weight @ np.transpose(trg_weight)
        self.gamma = np.reshape(self.gamma, -1)[:,np.newaxis]
        
        self.Lam_row = np.kron(np.eye(self.src_samples), np.ones(self.trg_samples))
        self.Lam_col = np.kron(np.ones(self.src_samples), np.eye(self.trg_samples))
        self.Lam = np.concatenate((self.Lam_row, self.Lam_col), axis = 0)
        
        self.mu = np.ones(self.src_samples + self.trg_samples)[:,np.newaxis]
        self.psi = np.ones(self.src_samples * self.trg_samples)[:,np.newaxis]
        
    def update_pi(self):
        temp = self.rho * (self.gamma + np.transpose(self.Lam) @ self.weight) - self.psi - self.cost - np.transpose(self.Lam) @ self.mu
        self.pi = 1/self.rho * np.linalg.inv(np.transpose(self.Lam) @ self.Lam + np.eye(self.src_samples * self.trg_samples)) @ temp
    
    def update_gamma(self):
        for i in range(self.gamma.shape[0]):
            self.gamma[i] = max(0, self.pi[i] + 1/self.rho * self.psi[i])
            
    def update_mu(self):
        self.mu = self.mu + self.rho * (self.Lam @ self.pi - self.weight)
        
    def update_psi(self):
        self.psi = self.psi + self.rho * (self.pi - self.gamma)
    
    def fit(self, iteration = 100):
        for epoch in range(iteration):
            self.update_pi()
            self.update_gamma()
            self.update_mu()
            self.update_psi()

n_sample = 3

source_data = np.array([[-1, 1],
                        [0,  0],
                        [1, -1]])

target_data = np.array([[0,  2.5],
                        [1,  1],
                        [2,  0]])

src_weight = np.array([1/3, 1/3, 1/3])[:,np.newaxis]
trg_weight = np.array([1/3, 1/3, 1/3])[:,np.newaxis]

ot_admm = OT_ADMM()
ot_admm.load_data(source_data, target_data, src_weight, trg_weight, rho = 10)
ot_admm.fit()
