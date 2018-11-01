
import numpy as np
import random

class MultiNetwork():

    def __init__(self,
                 layer_dims,
                 weight_decay):
        self.parameter = {}
        self.decay = weight_decay
        self.batch_norm = {}

        L = len(layer_dims)

        for i in range(1,L):
            self.parameter['W'+str(i)] = np.random.rand(layer_dims[i-1],
                                                        layer_dims[i])/np.sqrt(layer_dims[i-1])
            self.parameter['b'+str(i)] = np.zeros([1,layer_dims[i]])
            assert(self.parameter['W'+str(i)].shape == (layer_dims[i-1],layer_dims[i]))
            assert(self.parameter['b'+str(i)].shape == (1,layer_dims[i]))
            self.batch_norm['gamma'+str(i)] = 1
            self.batch_norm['beta'+str(i)] = 1

    def _sigmoid(self,z):
        return 1/(1+np.exp(-z))

    def _diff_sigmoid(self,z):
        return self._sigmoid(z)*(1-self._sigmoid(z))

    def _tanh(self,z):
        return (np.exp(z)+np.exp(-z))/(np.exp(z)-np.exp(-z))

    def _diff_tanh(self,z):
        return 1 - self._tanh(z)**2

    def _relu(self,z):
        return np.maximum(0,z)

    def _diff_relu(self,z):
        dz = np.array(z,copy = True)
        dz[z > 0] = 1
        dz[z <= 0] = 0
        return dz

    def linear_forward(self,
                       input,
                       weight,
                       bias):
        z = np.dot(input,weight) + bias
        assert(z.shape == (input.shape[0],weight.shape[1]))
        return z

    def linear_activation_forward(self,
                                  input,
                                  weight,
                                  bias,
                                  method,
                                  current_layer):
        temp = self.linear_forward(input,weight,bias)
        z = self.batch_norm['gamma'+str(current_layer)] * (temp-np.mean(temp))/np.std(temp) + self.batch_norm['beta'+str(current_layer)]
        self.norm_cache['X'+str(current_layer)] = (temp-np.mean(temp))/np.std(temp)
        self.norm_std['X'+str(current_layer)] = np.std(temp)
        if method == 'sigmoid':
            a = self._sigmoid(z)
        if method == 'relu':
            a = self._relu(z)
        if method == 'tanh':
            a = self._tanh(z)
        if method == 'none':
            a = z
        return a

    def forward(self,
                data):
        self.backparameter = {}
        self.cache = {}
        self.droplist = {}
        self.norm_cache = {}
        self.norm_std = {}

        input = data
        L = len(self.parameter)//2

        for i in range(1,L):
            input_pre = input
            self.cache['X'+str(i)] = input_pre
            input = self.linear_activation_forward(input_pre,
                                                   self.parameter['W'+str(i)],
                                                   self.parameter['b'+str(i)],
                                                   'relu',
                                                   current_layer = i)
            total_drop = int(dropout * self.parameter['W'+str(i)].shape[1])
            self.droplist['layer'+str(i)] = random.sample(range(0,self.parameter['W'+str(i)].shape[1]),
                                                          total_drop)
            for dt in self.droplist['layer'+str(i)]:
                input[:,dt] = 0

            self.backparameter['diff'+str(i)] = self._diff_relu(input)

        self.cache['X'+str(L)] = input
        output = self.linear_activation_forward(input,
                                                self.parameter['W'+str(L)],
                                                self.parameter['b'+str(L)],
                                                'none',
                                                current_layer = L)
        self.backparameter['diff'+str(L)] = 1
        return output

    def compute_loss(self,
                     output,
                     label,
                     method):
        if method == 'softmax':
            q = np.array(output,copy = True)
            for i in range(output.shape[0]):
                sum = np.sum(np.exp(output[i]))
                for j in range(output.shape[1]):
                    q[i][j] = np.exp(output[i][j])/(sum)
            loss = q - label
            print(q)
        if method == 'mse':
           loss = output - label
        return loss

    def backward(self,
                 loss):
        self.gradient = {}
        L = len(self.parameter)//2

        self.gradient['dbeta' + str(L)] = loss*np.sum(self.backparameter['diff'+str(L)])
        self.gradient['dgamma' + str(L)] = loss*np.sum(self.backparameter['diff'+str(L)]*self.norm_cache['X'+str(L)])
        self.gradient['db' + str(L)] = loss*self.backparameter['diff'+str(L)]
        self.gradient['dW' + str(L)] = np.dot(self.cache['X'+str(L)].T,
                                              self.gradient['db' + str(L)]) + \
                                              self.decay*self.parameter['W'+str(L)]
        self.gradient['dA' + str(L)] = np.dot(self.gradient['db' + str(L)],
                                              self.parameter['W'+str(L)].T)
        for i in reversed(range(1,L)):
            self.gradient['dbeta' + str(i)] = np.sum(self.gradient['dA' + str(i+1)]*self.backparameter['diff'+str(i)])
            self.gradient['dgamma' + str(i)] = np.sum(self.gradient['dA' + str(i+1)]*self.backparameter['diff'+str(i)]*self.norm_cache['X'+str(i)])
            self.gradient['db' + str(i)] = self.gradient['dA' + str(i+1)]*self.backparameter['diff'+str(i)]
            self.gradient['dW' + str(i)] = np.dot(self.cache['X'+str(i)].T,
                                                  self.gradient['db' + str(i)])+ \
                                                  self.decay*self.parameter['W'+str(i)]
            self.gradient['dA' + str(i)] = np.dot(self.gradient['db' + str(i)],
                                                  self.parameter['W'+str(i)].T)
    def update(self,
               studyratio,
               dropout):
        L = len(self.parameter)//2

        for i in range(1,L+1):
            if(i < L):
                for dt in self.droplist['layer'+str(i)]:
                    self.gradient['dW'+str(dt)] = 0
                    self.gradient['db'+str(dt)] = 0

            self.batch_norm['gamma'+str(i)] = self.batch_norm['gamma'+str(i)] - studyratio*self.gradient['dgamma'+str(i)]
            self.batch_norm['beta'+str(i)] = self.batch_norm['beta'+str(i)] - studyratio*self.gradient['dbeta'+str(i)]
            self.parameter['W'+str(i)] = self.parameter['W'+str(i)] - studyratio*self.gradient['dW'+str(i)]
            self.parameter['b'+str(i)] = self.parameter['b'+str(i)] - studyratio*self.gradient['db'+str(i)]

    def train(self,
              data,
              label,
              studyratio,
              dropout = 0):
        output = self.forward(data)
        loss = self.compute_loss(output,label,'softmax')
        self.backward(loss)
        self.update(studyratio,dropout)

data = np.array([[1.0,1.0],[0.0,0.0],[0.0,1.0],[1.0,0.0]])
label = np.array([[1.0,0.0],
                  [1.0,0.0],
                  [0.0,1.0],
                  [0.0,1.0]])
studyratio = 0.1
dropout = 0.01
weight_decay = 0.001
Layers = [2,2,2]
bp = MultiNetwork(Layers,weight_decay)
for iteration in range(1,10000):
    bp.train(data,label,studyratio,dropout)
