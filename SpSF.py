
# coding: utf-8

# In[10]:

import matplotlib
import pylab as pl
import random as rd
import numpy as np
import networkx as nx
import scipy as sp
from scipy import stats
from collections import Counter
from Plfit2 import plfit
from __future__ import division


# In[2]:

# n = population size
# density = density of the grid cell
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

def Select(net,new,m,alpha):
    deg = nx.degree(net).values()
    new_coord = np.where(agents == new)
    nodeJ_coord = list()
    targets = list()
    exponent = alpha * (-1)
    while len(targets) < m:
        nodeJ = rd.randint(0,len(deg)-1)
        while nodeJ in targets:
            nodeJ = rd.randint(0,len(deg)-1)
        nodeJ_coord = np.where(agents == nodeJ)
        d = (float(nodeJ_coord[0] - new_coord[0])**2 + (float(nodeJ_coord[1] - new_coord[1])**2))**0.5
        d_alpha = d**(exponent)
        ConnPr = d_alpha * deg[nodeJ]
        chance = rd.random()
        if (ConnPr <= 1 and ConnPr > chance):
            targets.append(nodeJ)
    return targets


# In[4]:

def SpatialNetSF(m,alpha):
    network = nx.empty_graph(m)
    targets = list(range(m))
    source = m
    while source < pop-1:
        network.add_edges_from(zip([source]*m,targets))
        source += 1
        targets = Select(network,source,m,alpha)
    return network
