# -*- coding: utf-8 -*-
"""
Implementación de grafo, tanto dirigido como no dirigido, 
para la ibreria de grafos.

Autor: Francisco Manuel Valle Ruiz

Última actualizacion: creación
"""

import random

##########################################
##########################################
#####                                #####
#####             Graph              #####
#####                                #####
##########################################
##########################################
class Graph:
    def __init__(self, name_='', directed=False, copy_of=None):
        """
        use directed = True if working with directed graphs
        copy_of is a graph
        """
        if isinstance(copy_of, Graph):
            self.copy(copy_of)
        else:
            self.name = name_
            self.nodes = {}
            self.directed = directed

    def __contains__(self, node):
        return (node in self.nodes)

    def __str__(self):
        def node2str(n):
            if n in self:
                node_str = str(n) + " : " + str(self.nodes[n])
                return node_str
            else:
                return False
                
        graph_str = "Graph name: "+ self.name + "\n"
        if len(self) == 0:
            graph_str += "- Empty Graph -\n"
        else:
            for n in self.nodes:
                graph_str += node2str(n) + "\n"
        return graph_str
    
    def __len__(self):
        return len(self.nodes)

    def __iter__(self):
        return iter(self.nodes.keys())

    def __add__(self, G):
        S = Graph(copy_of=self)
        if isinstance(G, Graph):
            for node in G.getNodes():
                for edge in G.getEdges(node):
                    S.addEdge(node, edge, G.getWeight(node, edge))
            return S
            
        return False

    def countEdges(self, node=None):
        if node:
            return len(self.nodes[node])
        
        else:
            if self.directed:
                return sum(map(lambda x: len(self.nodes[x]), self.getNodes()))
            else:
                return sum(map(lambda x: len(self.nodes[x]), self.getNodes()))/2

    def degree(self, n = None):
        return len(self.getEdges(n))

    def size(self):
        return len(self.nodes)
        
    def weight(self):
        w = 0
        for n in self.nodes.values():
            w += sum(n.values())
        if not self.directed:
            w = w/2
            
        return w
    
    def rename(self, new_name):
        self.name = new_name

    def is_same_size(self, obj):
        return len(self) == len(obj)
    
    def copy(self, G = None):
        if G is None:
            G = self
        self.name = G.getName()
        self.nodes = G.getNodes()
        self.directed = G.directed
    
    def getName(self):
        return self.name

    def getNodes(self):
        return self.nodes.copy()

    def getWeight(self, n1, n2):
        """
        Gets the weight of the arc joining n1 and n2
        
        If n1 and n2 is the same node, and it has no loops
        then return 0 
        (I don't think that doing this is completely right 
        semantically, but the cost of going from n1 to n1 is 0,
        so this behavior comes handy)

        If n1 and n2 are in the graph, but are not adjacent,
        returns infinite

        if n1 or n2 are not in the graph, returns False
        """
        if n1 in self and n2 in self:
            if n2 in self.nodes[n1]:
                return self.nodes[n1][n2]
            elif n1 == n2:
                return 0
            return float("inf")
        return False

    def getEdges(self, n = None):
        if n:
            if n in self:
                return self.nodes[n]
            else:
                return None
        edges = []
        for n in self:
            for v in self.nodes[n]:
                edges.append( (n, v, self.nodes[n][v]) )
        return edges


    def is_directed(self):
        return self.directed

    def is_not_directed(self):
        return not self.directed
    
    def addEdge(self, n1, n2, weight=1):
        if not n1 in self.nodes:
            self.nodes[n1] = {}
        self.nodes[n1][n2] = weight

        if self.directed is False:
            if not n2 in self.nodes:
                self.nodes[n2] = {}
            self.nodes[n2][n1] = weight

        return True

    def hasEdge(self, e):
        n1, n2 = e
        return n2 in self.nodes[n1]

    def add(self, n, G = None):
        """
        n is a string (the node's name)
        G is a graph (if user wants to copy instead of create a new node)
        
        returns a dictionary that represents the node
        """
        if not n in self:
            self.nodes[n] = {}

        if G:
            if n in G:
                self.nodes[n] = G.getEdges(n)
    
    def addNodes(self, list_nodes, G = None):
        for n in list_nodes:
            self.add(n, G)

    def random_node(self):
        n = random.choice(self.nodes.keys())
        return (n, self.nodes[n])