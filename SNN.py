import numpy as np
import random
from copy import deepcopy
from random import shuffle
from numpy import dot, outer


class SoftmaxNeuralNetwork:
    def __init__(self, input_dim=729, hidden_dim=27, output_dim=3, afunc=np.tanh, d_afunc=(lambda z : 1.0 - z**2)):        
        self.afunc = afunc 
        self.d_afunc = d_afunc      
        self.input = np.ones(input_dim)                                         
        self.hidden = np.ones(hidden_dim+1)      
        self.output = np.ones(output_dim)
        self.predictions = np.ones(output_dim)
        self.iweights = np.random.normal(scale=0.0001, size=(input_dim, hidden_dim))
        self.oweights = np.random.normal(scale=0.0001, size=(hidden_dim+1, output_dim)) 
        self.ierr = np.zeros(self.iweights.shape)
        self.oerr = np.zeros(self.oweights.shape)
        self.imom = np.zeros(self.iweights.shape)
        self.omom = np.zeros(self.oweights.shape)
        
    def forward_propagation(self, ex):
        self.input = ex
        self.hidden[:-1] = self.afunc(dot(self.input, self.iweights))
        self.output = np.exp(dot(self.hidden, self.oweights))
        self.output /= np.sum(self.output)
        self.output -= np.max(self.output)
        self.predictions = np.sign(self.output)+1
        
    def backward_propagation(self, labels, alpha=0.5):
        labels = np.array(labels)
        oerr = labels-self.predictions
        herr = dot(oerr, self.oweights.T) * self.d_afunc(self.hidden)
        self.oweights += alpha * outer(self.hidden, oerr)
        self.iweights += alpha * outer(self.input, herr[:-1])
        return 0.5 * np.sum(np.abs(labels-self.predictions))

    def train(self, training_data, maxiter=5000, alpha=0.05, lmbda=0, epsilon=1.5e-8, display_progress=False):       
        iteration = 0
        error = sys.float_info.max
        while error > epsilon and iteration < maxiter:
            gamma = 1/(2+math.trunc(np.sqrt(iteration)))
            error = 0.0
            size = 0.0
            shuffle(training_data)
            for ex, labels in training_data:
                self.forward_propagation(ex)
                size += abs(self.output)
                error += self.backward_propagation(labels, alpha=alpha)
                self.imom = self.ierr + gamma*self.imom
                self.omom = self.oerr + gamma*self.omom
#                 self.iweights += self.imom #- lmbda*self.l2penalty(self.iweights)
#                 self.oweights += self.omom #- lmbda*self.l2penalty(self.oweights)
                self.iweights = self.iweights*(1-lmbda)
                self.oweights = self.oweights*(1-lmbda)
            if display_progress and iteration%10==0:
                print 'completed iteration %s; error is %s; size is %s' % (iteration, error, np.sum(np.absolute(self.iweights)))
            iteration += 1
            
    def accuracy(self, data):
        score = 0.0
        for ex, label in data:
            self.forward_propagation(ex)
#             print self.predictions, np.array(label), self.predictions-np.array(label)
            if np.sum(np.multiply(self.predictions, np.array(label)))==1: score+=1
        return score/len(data)
            
    def l2penalty(self, arr):
        return np.multiply(np.array(map(lambda x: linalg.norm(arr[:,x]), range(len(arr[0])))), arr)
                    
    def predict(self, ex):
        self.forward_propagation(ex)
        return deepcopy(self.output)
        
    def hidden_representation(self, ex):
        self.forward_propagation(ex)
        return self.hidden