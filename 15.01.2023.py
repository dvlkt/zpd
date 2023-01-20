from random import *
from math import *
import pygame
values=[randint(0,100)/100 for i in range(10)]
# max neurons ne mazāku par 2
class Network:
    def __init__(self,bildes_lielums=[16,32],layers=2,max_neurons=5):
        self.neurons=[]
        self.bildes_lielums=bildes_lielums
        self.max_neurons=max_neurons
        self.layers=layers
        for i in range(layers):
            layer=[]
            for i1 in range(randint(2,max_neurons)):
                layer.append(Neuron(self,i,bildes_lielums))
            self.neurons.append(layer)
    def process(self,bilde):
        self.bilde=bilde
        for i in self.neurons:
            for i1 in i:
                i1.think()
    def draw(self):
        pygame.init()
        S=pygame.Surface((self.layers*60-40,self.max_neurons*30))
        pcount=self.max_neurons
        for i in range(self.layers):
            if i!=0:
                poffset=offset
            offset=(self.max_neurons-len(self.neurons[i]))*15
            for i1 in range(len(self.neurons[i])):
                pygame.draw.rect(S,(255,255,255),(5+i*60,5+offset+i1*30,20,20))
                if i!=0:
                    for i2 in range(len(self.neurons[i][i1].inputs)):
                        pygame.draw.line(S,(255,255,255),(15+i*60,15+offset+i1*30),(i*60-45,poffset+15+self.neurons[i][i1].inputs[i2][0]*30))
                        #print(self.neurons[i][i1].inputs[i2][0])
                        
        pygame.image.save(S,"Neural Network.png")
class Neuron:
    def __init__(self,owner,layer,bildes_lielums):
        self.layer=layer
        self.inputs=[]
        self.bildes_lielums=bildes_lielums
        self.owner=owner
        if self.layer==0:
            itaken=[]
            for i in range(randint(2,owner.max_neurons)):
                #x,y,weight
                coords=[randint(0,bildes_lielums[0]-1),randint(0,bildes_lielums[1]-1)]
                if coords not in itaken:
                    self.inputs.append([coords,randint(1,10000)/1000*(randint(0,1)*2-1)])
                    itaken.append(coords)
        else:
            itaken=[]
            for i in range(randint(2,len(owner.neurons[self.layer-1]))):
                inpu=randint(0,len(owner.neurons[self.layer-1])-1)
                if inpu not in itaken:
                    self.inputs.append([inpu,randint(1,10000)/1000*(randint(0,1)*2-1)])
                    itaken.append(inpu)
        self.bias=randint(0,100)/100
        self.value=0
    def think(self):
        self.value=self.bias
        self.bilde=self.owner.bilde
        if self.layer==0:
            for i in range(len(self.inputs)):
                self.value+=self.bilde[self.inputs[i][0][0]][self.inputs[i][0][1]]*self.inputs[i][1]
        else:
            for i in range(len(self.inputs)):
                self.value+=self.inputs[i][1]*self.owner.neurons[self.layer-1][self.inputs[i][0]].value
        self.value=1/(1+e**(-self.value))
n=Network([8,8],5,5)
n.process([[randint(1,1000)/100 for i in range(8)] for i in range(8)])
n.draw()
