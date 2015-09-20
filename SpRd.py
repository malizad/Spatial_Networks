
# coding: utf-8

# In[1]:

import matplotlib
import pylab as pl
import random as rd
import numpy as np
import networkx as nx
from scipy import stats
import scipy as sp


# In[2]:

def init(n,density):
    global agents, pop
    width = int(round((n/density)**0.5))
    height = int(round((n/density)**0.5))
    config = np.zeros([height, width])
    pop = 0 #actual population size
    for x in range(height):
        for y in range(width):
            if rd.random() < density:
                config[x,y] = 1
                pop += 1

    # Populating the agents matrix with a random sequence of agents
    seq = [x for x in range(pop)]
    rd.shuffle(seq)
    agents = np.zeros([height, width])
    for r in range(height):
        for t in range(width):
            if agents[r,t] == 0:
                agents[r,t] = -1
    z = 0
    for i in range(height):
        for j in range(width):
            if config[i,j] == 1:
                agents[i,j]=seq[z]
                z += 1


# In[3]:

def Pr_Con(a,c,node1, node2):
    coord1 = np.where(agents == node1)
    coord2 = np.where(agents == node2)
    dist = sqrt (int(coord1[0] - coord2[0])**2 + (int(coord1[1] - coord2[1])**2))
    pr = c * (dist**(-a))
    return pr


# In[4]:

def SpRd(c,a):
    network = nx.Graph()
    for node in range(1,pop):
        network.add_node(node)
    for node1 in range(1,pop):
        for node2 in range(node1 + 1,pop):
            chance = rd.random()
            Pr_Connection = Pr_Con(a,c,node1,node2)
            if chance < Pr_Connection:
                network.add_edge(node1,node2)
    return network
