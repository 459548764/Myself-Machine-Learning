class OT_BADMM():
    def __init__(self):
        pass
    
    def load_data(self, src_data, trg_data, src_weight, trg_weight, rho):
        self.src_data = src_data
        self.trg_data = trg_data
        self.rho = rho
        
        self.src_samples = self.src_data.shape[0]
        self.trg_samples = self.trg_data.shape[0]
        self.src_weight = src_weight
        self.trg_weight = trg_weight
        
        self.cost = ot.dist(self.src_data, self.trg_data)
        self.gamma = src_weight @ np.transpose(trg_weight)
        self.pi = src_weight @ np.transpose(trg_weight)
        
        self.Lam = np.ones([self.src_samples, self.trg_samples])
    
    def update_pi(self): 
        for i in range(self.src_samples):
            for j in range(self.trg_samples):
                temp = 0
                for k in range(self.trg_samples):
                    temp += np.exp( (-self.cost[i][k] - self.Lam[i][k]) / self.rho ) 
                    
                self.pi[i][j] = np.exp( (-self.cost[i][j] - self.Lam[i][j]) / self.rho )  / temp * self.src_weight[i]
    
    def update_gamma(self):
        for i in range(self.src_samples):
            for j in range(self.trg_samples):
                temp = 0
                for k in range(self.src_samples):
                    temp += np.exp( self.Lam[k][j] / self.rho ) 
            
                self.gamma[i][j] = np.exp( self.Lam[i][j] / self.rho ) / temp * self.trg_weight[j]
    
    def update_lam(self):
        self.Lam = self.Lam + self.rho * (self.pi - self.gamma)
        
    def fix(self, iteration = 200):
        for epoch in range(iteration):
            self.update_pi()
            self.update_gamma()
            self.update_lam() 
            print(self.pi)
            
n_sample = 3

source_data = np.array([[-1, 1],
                        [0,  0],
                        [1, -1]])

target_data = np.array([[0,  2],
                        [1,  1],
                        [2,  0]])

src_weight = np.array([1/3, 1/3, 1/3])[:,np.newaxis]
trg_weight = np.array([1/3, 1/3, 1/3])[:,np.newaxis]

ot_badmm = OT_BADMM()
ot_badmm.load_data(source_data, target_data, src_weight, trg_weight, rho = 1)
ot_badmm.fix()
