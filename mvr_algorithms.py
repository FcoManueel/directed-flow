# -*- coding: utf-8 -*-
"""
Implementación de algoritmos sobre grafos.

Autor: Francisco Manuel Valle Ruiz

Última actualizacion: Prim y Kruskal
"""
import random
from collections import deque
from Queue import PriorityQueue

from mvr_graph import *
from mvr_edge_queue import *
from mvr_utils import *
        
##########################################
##########################################
#####                                #####
#####        Graph Algorithms        #####
#####                                #####
##########################################
##########################################


####################################################
###                  searches                    ###
####################################################
def bfs(G):
        #n, _ = G.random_node()
        if len(G) == 0:
            return None
            
        n = sorted(G.nodes.keys())[0]
        print "Comenzando con: ", n
        spanning_tree = Graph()
        queue = deque()
        
        spanning_tree.add(n)
        queue.append(n)
        while queue:
            v = queue.popleft()
            #print "Revisando: ", v
            for neigh in sorted(G.nodes[v].keys()):
                if neigh not in spanning_tree.getNodes():
                    #print "---Agregando: ", neigh
                    spanning_tree.add(neigh)
                    spanning_tree.addEdge(v, neigh)
                    #print "---tree so far:",spanning_tree
                    #print "-"*20
                if spanning_tree.is_same_size(G):
                    return spanning_tree
                else:
                    queue.append(neigh)
        
        return (spanning_tree if spanning_tree.is_same_size(G) else
                None)

def dfs(G):
    return dfs_it(G)

def dfs_it(G): #Iterative implementation
    if len(G) == 0:
        return None

    #n, _ = G.random_node()
    
    spanning_tree = Graph("Arbol de expansión, depth-first search iterativo")
    stack = deque()
    
    n = sorted(G.nodes.keys())[0]
    spanning_tree.add(n)

    while True:
        edges_not_in_tree = filter(lambda neigh: neigh not in spanning_tree, sorted(G.nodes[n].keys()))
        if edges_not_in_tree:
            neigh = edges_not_in_tree[0]
            spanning_tree.add(neigh)
            spanning_tree.addEdge(n, neigh)
            stack.append(n)
            if spanning_tree.is_same_size(G):
                    return spanning_tree
            n = neigh
        elif stack:
            n = stack.pop()
        else:
            return (spanning_tree if spanning_tree.is_same_size(G) else None)

def dfs_re(G): # Recursive implementation
    def dfs_recursive(G, n, spanning_tree):
        for neigh in G.nodes[n]:
            if neigh not in spanning_tree:
                spanning_tree.add(neigh)
                spanning_tree.addEdge(n, neigh)
                #print "Llamando a funcion con " + str(neigh) + "y con " + str(spanning_tree)
                dfs_recursive(G, neigh, spanning_tree)             

    n, _ = G.random_node()
    spanning_tree = Graph("Arbol de expansion, depth-first search recursivo")
    spanning_tree.add(n)
    dfs2_recursive(G, n, spanning_tree)
    return (spanning_tree if spanning_tree.is_same_size(G) else None)

####################################################
###              min-expansion trees             ###
####################################################
def prim(G): # For minimum expansion tree
    # Create tree
    T = Graph("Prim's minimum spanning tree of "+G.getName(), directed=G.is_directed())

    # Create priority queue and auxiliar function to mark edges
    edges_queue = EdgePriorityQueue()
    def mark_edges(n):
        n_edges = G.getEdges(n)
        for v in n_edges:
            if v not in T:
                # "mark" (put in e.p.queue) all the edges connecting n and nodes not in T
                print "Marcando arista: "+str((n,v,n_edges[v]))
                edges_queue.put( (n, v), n_edges[v])

    # Add first element (n) to T and mark edges
    n, _ = G.random_node()
    T.add(n)
    mark_edges(n)


    while(len(T) != len(G)):        
        if not edges_queue.empty():
            edge, w = edges_queue.get()
            n1, n2 = edge
            if n2 not in T:
                T.addEdge(n1, n2, w)
                #print "Se agrego una arista a T: ", (n1,n2,w)
                #print "T quedo asi: ",T
                mark_edges(n2)
        else:
            print "Al parecer no existe 'prim'. Este es el estado de las cosas:"
            print T
            return None
    return T

def kruskal(G): # For minimum expansion forest
    """
    Recibe un grafo y devuelve un arreglo que contiene los arboles que
    conforman el bosque de mínima expansión. Si la gráfica es conexa
    el arreglo contiene una sola gráfica.
    """
    edges_queue = EdgePriorityQueue(G)
    forest = []

    def in_forest(n):
        for tree in forest:
            for node in tree:
                if n == node or n in tree.nodes[node]:
                    return True
        return False

    def get_tree(n):
        for tree in forest:
            for node in tree.nodes:
                if n == node or n in tree.nodes[node]:
                    return tree
        return False
    
    def success_tree():
        successful = None
        for tree in forest:
            if tree.countEdges() == (len(G)-1):
                successful = tree
        return successful
    
    tree_num = 0
    while( not edges_queue.empty() ):
        e, w = edges_queue.get()
        n1, n2 = e
        
        t1 = get_tree(n1)
        t2 = get_tree(n2)
        
        if not t1 and not t2: # los extremos no estan en arboles
            new_tree = Graph("AuxTree "+str(tree_num), directed=G.directed)
            tree_num += 1
            new_tree.addEdge(n1,n2, w)
            forest.append(new_tree)
        elif ((not t1 and t2) or (t1 and not t2)):
            if t1:
                t1.addEdge(n1, n2, w) # checar si n1, n2 estan en orden correcto
            else:
                t2.addEdge(n1, n2, w) # checar si n1, n2 estan en orden correcto
        
        elif t1 != t2: # mezclar t1 y t2
            t1_index = forest.index(t1)
            
            t1 = t1+t2
            t1.addEdge(n1,n2,w)
            
            forest[t1_index] = t1
            forest.remove(t2)
        
        # elif  t1 == t2: # ignorar arista por confilcto de ciclos

    # Hice algunos cambios en esta ultima parte pero no los revise. Si hay algun
    # error, revisar aqui:
    for i, tree in enumerate(forest):
        tree.rename(G.name + "'s Least-Weight Spanning Tree (Kruskal) - " + str(i))
    return forest