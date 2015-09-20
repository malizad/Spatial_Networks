
# coding: utf-8

# In[1]:

import matplotlib
import pylab as pl
import random as rd
import numpy as np
import networkx as nx


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

def SpatialSW2(p,k,a):
    global u,v,j,w,G,targets,nodes
    G = nx.Graph()
    nodes = list(range(pop)) # nodes are labeled 0 to n-1
    # connect each node to k/2 neighbors
    for j in range(1, k // 2+1):
        targets = nodes[j:] + nodes[0:j] # first j nodes are now last in list
        G.add_edges_from(zip(nodes,targets))
    # rewire edges from each node
    # loop over all nodes in order (label) and neighbors in order (distance)
    # no self loops or multiple edges allowed
    for j in range(1, k // 2+1): # outer loop is neighbors
        targets = nodes[j:] + nodes[0:j] # first j nodes are now last in list
        # inner loop in node order
        for u,v in zip(nodes,targets): 
            if rd.random() < p:
                chosen = False
                while chosen == False:
                    w = rd.choice(nodes)
                    while w == u or G.has_edge(u, w): # Enforce no self-loops or multiple edges
                        w = rd.choice(nodes)
                    u_coord = np.where(agents == u)
                    w_coord = np.where(agents == w)
                    d = (float(u_coord[0] - w_coord[0])**2 + (float(u_coord[1] - w_coord[1])**2))**0.5
                    q = 0.5 * (d)**(-a)
                    if rd.random() < q:
                        G.remove_edge(u,v)  
                        G.add_edge(u,w)
                        chosen = True
    return G


# In[4]:

def SpSW(k,a):
    global u,v,j,w,G,targets,nodes
    G = nx.Graph()
    nodes = list(range(pop)) # nodes are labeled 0 to n-1
    # connect each node to k/2 neighbors
    for j in range(1, k // 2+1):
        targets = nodes[j:] + nodes[0:j] # first j nodes are now last in list
        G.add_edges_from(zip(nodes,targets))
    # rewire edges from each node
    # loop over all nodes in order (label) and neighbors in order (distance)
    # no self loops or multiple edges allowed
    for j in range(1, k // 2+1): # outer loop is neighbors
        targets = nodes[j:] + nodes[0:j] # first j nodes are now last in list
        # inner loop in node order
        for u,v in zip(nodes,targets): 
            u_coord = np.where(agents == u)
            v_coord = np.where(agents == v)
            d = (float(u_coord[0] - v_coord[0])**2 + (float(u_coord[1] - v_coord[1])**2))**0.5
            p = (d)**(-a)
            if rd.random() < p:
                w = rd.choice(nodes)
                while w == u or G.has_edge(u, w): # Enforce no self-loops or multiple edges
                    w = rd.choice(nodes)
                G.remove_edge(u,v)  
                G.add_edge(u,w)
    return G
