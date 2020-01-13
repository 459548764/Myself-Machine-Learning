import numpy as np

def load():
    data = np.array([[3,8,8,3,6,6,2,1,9,4,5,8,4,3,2],
                     [8,8,3,8,3,5,2,1,5,7,4,3,2,6,1],
                     [5,8,3,8,4,8,9,1,2,9,7,5,4,2,1]])
    label = np.array([-1,1,-1,-1,-1,1,-1,-1,-1,1,1,1,-1,-1,-1])
    return data,label

class Weak_Classify():
    def __init__(self,x,y):
        '''
        :param n: Features
        :param sample: Batch-size
        '''
        self.x = np.array(x)
        self.y = np.array(y)
        self.n = self.x.shape[0]
        self.sample = self.x.shape[1]

    def train(self,weights):
        self.weights = weights
        min = 100000
        threshold_value = 0
        threshold_feature = 0
        threshold_direction = 0

        for i in range(self.n):
            value,errcnt = self.findmin(i,1)
            if errcnt < min:
                min = errcnt
                threshold_value = value
                threshold_feature = i
                threshold_direction = 1
        for i in range(self.n):
            value,errcnt = self.findmin(i,-1)
            if errcnt < min:
                min = errcnt
                threshold_value = value
                threshold_feature = i
                threshold_direction = -1
        wc = {
            'threshold_value':threshold_value,
            'threshold_feature':threshold_feature,
            'threshold_direction':threshold_direction
        }
        return min,wc

    def findmin(self,feature,direction):
        buttom = np.min(self.x[feature])
        up = np.max(self.x[feature])

        minerr = 100000
        value = 0
        for t in range(buttom,up):
            errcnt = self.check(feature,direction,t)
            if errcnt < minerr:
                minerr = errcnt
                value = t
        return value,minerr

    def check(self,feature,direction,threshold):
        errcnt = 0
        logit = np.zeros([self.sample])
        for i in range(self.sample):
            if(direction == 1):
                if(self.x[feature][i] < threshold):
                    logit[i] = -1
                else:
                    logit[i] = 1
            else:
                if(self.x[feature][i] < threshold):
                    logit[i] = 1
                else:
                    logit[i] = -1

            if(logit[i] != self.y[i]):
                errcnt += self.weights[i]
        return errcnt

class Adaboost():
    def __init__(self,x,y):
        self.x = np.array(x)
        self.y = np.array(y)
        self.weight = np.ones((self.x.shape[1],1)).flatten(1)/self.x.shape[1]

    def predict(self,sample,idx):
        threshold_value = self.G[idx]['threshold_value']
        threshold_feature = self.G[idx]['threshold_feature']
        threshold_direction = self.G[idx]['threshold_direction']
        if(self.x[threshold_feature][sample] < threshold_value and threshold_direction == -1):
            return 1
        elif(self.x[threshold_feature][sample] < threshold_value and threshold_direction == 1):
            return -1
        elif(self.x[threshold_feature][sample] >= threshold_value and threshold_direction == 1):
            return 1
        else:
            return -1

    def train(self,M = 5):
        self.G = {}
        self.alpha = {}
        for i in range(M):
            self.G.setdefault(i)
            self.alpha.setdefault(i)

        for i in range(M):
            temp = Weak_Classify(self.x,self.y)
            err,self.G[i] = temp.train(self.weight)
            print(self.G[i],err)
            self.alpha[i] = 1.0/2 * np.log((1-err)/err)

            pred_logit = np.zeros(self.x.shape[1])
            for m in range(self.x.shape[1]):
                temp = 0
                for n in range(i):
                    temp += self.alpha[i] * self.predict(m,n)
                if(temp <= 0):
                    pred_logit[m] = -1
                else:
                    pred_logit[m] = 1

            new_weight = self.weight
            weight_sum = 0
            for m in range(self.x.shape[1]):
                if(pred_logit[m] == self.y[m]):
                    new_weight[m] = self.weight[m] * np.exp(-self.alpha[i])
                else:
                    new_weight[m] = self.weight[m] * np.exp(self.alpha[i])
                weight_sum += new_weight[m]
            self.weight = new_weight/weight_sum
            print(pred_logit)
            print(self.weight)

x,y = load()
print(x.shape,y.shape)
ada = Adaboost(x,y)
ada.train()
