# -*- coding: utf-8 -*-
"""
Utilerias para la libreria de grafos
Autor: Francisco Manuel Valle Ruiz

Última actualizacion: creación
"""
from mvr_graph import *

####################################################
###                   prints                     ###
####################################################
def mprint(M):
    #M is a square matrix
    size = len(M)
    for y in xrange(size):
        print M[y]



####################################################
###                  creation                    ###
####################################################
def complete_graph(n):
    # Returns the complete graph of n vertices
    n = max(n,0)
    complete = Graph()
    complete.name = "Complete graph of "+ str(n) + " vertices"

    for i in range(n):
        complete.add(str(i))
        for j in range(i):
            complete.addEdge(str(i), str(j))
    return complete

def toMatrix(G): # Weight adjacency matrix
    size = len(G)
    
    # tags is a dictionary of the previous names of each node.
    # e.g. a possible tag value is  0:"node_name"
    #print zip(range(size),G.nodes[:])
    #    print "i:",i,"    n:",n
    tags = {i:n for i, n in zip(range(size),sorted(G.nodes.keys()))}
    matrix = [[float("inf") for _ in xrange(size)] for _ in xrange(size)] 

    for y in xrange(size):
        for x in xrange(size):
                matrix[y][x] = G.getWeight(tags[y], tags[x])
    return (matrix, tags)

####################################################
###                property-check                ###
####################################################
def is_bipartite(G):
    # Parte recursiva del algoritmo
    def recursive_bip(G, n, v_sets, v_index = 0):
        next_v_index = (v_index+1) % 2
        vecinos = G.nodes[n]
        to_check = []
        for w in vecinos:
            if w in v_sets[v_index]:
                return False
            
            if w not in v_sets[next_v_index]:
                v_sets[next_v_index].append(w)
                to_check.append(w)

        for node in to_check:
            if G.recursive_bip(node, v_sets, next_v_index) is False:
                return False

        return True

    V0 = []
    V1 = []
    v_sets = (V0, V1)
    all_check = False
    
    while(not all_check):
        n = random.choice(filter(lambda x: x not in V0 and x not in V1 ,G.nodes.keys()))
        V0.append(n)
        
        #print "Component check starting from node " + n.name
        bipartite = G.recursive_bip(n,v_sets)
        if (not bipartite): return False
        all_check = (len(V0) + len(V1)) is len(G)
        
    return True