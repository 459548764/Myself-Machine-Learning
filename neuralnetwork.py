
import numpy as np
import random

class MultiNetwork():

    def __init__(self,
                 layer_dims):
        self.parameter = {}
        L = len(layer_dims)

        for i in range(1,L):
            self.parameter['W'+str(i)] = np.random.rand(layer_dims[i-1],
                                                        layer_dims[i])/np.sqrt(layer_dims[i-1])
            self.parameter['b'+str(i)] = np.zeros([1,layer_dims[i]])
            assert(self.parameter['W'+str(i)].shape == (layer_dims[i-1],layer_dims[i]))
            assert(self.parameter['b'+str(i)].shape == (1,layer_dims[i]))

    def _sigmoid(self,z):
        return 1/(1+np.exp(-z))

    def _diff_sigmoid(self,z):
        return self._sigmoid(z)*(1-self._sigmoid(z))

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
                                  method):
        z = self.linear_forward(input,weight,bias)
        if method == 'sigmoid':
            a = self._sigmoid(z)
        if method == 'none':
            a = z
        return a

    def forward(self,
                data):
        self.backparameter = {}
        self.cache = {}

        input = data
        L = len(self.parameter)//2

        for i in range(1,L):
            input_pre = input
            self.cache['X'+str(i)] = input_pre
            input = self.linear_activation_forward(input_pre,
                                                   self.parameter['W'+str(i)],
                                                   self.parameter['b'+str(i)],
                                                   'sigmoid')
            self.backparameter['diff'+str(i)] = self._diff_sigmoid(input)

        self.cache['X'+str(L)] = input
        output = self.linear_activation_forward(input,
                                                self.parameter['W'+str(L)],
                                                self.parameter['b'+str(L)],
                                                'sigmoid')
        self.backparameter['diff'+str(L)] = self._diff_sigmoid(output)
        return output

    def compute_loss(self,
                     output,
                     label,
                     method):
        if method == 'softmax':
            loss = output - label
        print(output)
        return loss

    def backward(self,
                 loss):
        self.gradient = {}
        L = len(self.parameter)//2

        self.gradient['db' + str(L)] = loss*self.backparameter['diff'+str(L)]
        self.gradient['dW' + str(L)] = np.dot(self.cache['X'+str(L)].T,
                                         loss*self.backparameter['diff'+str(L)])
        self.gradient['dA' + str(L)] = np.dot(loss*self.backparameter['diff'+str(L)],
                                         self.parameter['W'+str(L)].T,)
        for i in reversed(range(1,L)):
            self.gradient['db' + str(i)] = self.gradient['dA' + str(i+1)]
            self.gradient['dW' + str(i)] = np.dot(self.cache['X'+str(i)].T,
                                                  self.gradient['dA' + str(i+1)])
            self.gradient['dA' + str(i)] = np.dot(self.gradient['dA' + str(i+1)],
                                                  self.parameter['W'+str(i)].T)

    def update(self,
               studyratio,
               dropout):
        L = len(self.parameter)//2

        for i in range(1,L+1):
            total_drop = int(dropout * self.parameter['W'+str(i)].shape[1])
            resultList = random.sample(range(0,self.parameter['W'+str(i)].shape[1]),
                                       total_drop)
            for dt in resultList:
                self.gradient['dW'+str(dt)] = 0
                self.gradient['db'+str(dt)] = 0

            self.parameter['W'+str(i)] = self.parameter['W'+str(i)] - studyratio*self.gradient['dW'+str(i)]
            self.parameter['b'+str(i)] = self.parameter['b'+str(i)] - studyratio*self.gradient['db'+str(i)]

    def train(self,
              data,
              label,
              studyratio,
              dropout = 0,
              iteration = 2000):
        for i in range(iteration):
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
Layers = [2,4,4,2]
bp = MultiNetwork(Layers)
bp.train(data,label,studyratio,0.25,2000)





