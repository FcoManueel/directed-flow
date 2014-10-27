# -*- coding: utf-8 -*-
"""
Implementación de cola de prioridad para uso especifico 
con aristas ponderadas, para la ibreria de grafos

Autor: Francisco Manuel Valle Ruiz

Última actualizacion: EdgePriorityQueue
"""
from Queue import PriorityQueue
from mvr_graph import *
from mvr_utils import *

##########################################
##########################################
#####                                #####
#####       Edge Priority Queue      #####
#####                                #####
##########################################
##########################################
class EdgePriorityQueue(PriorityQueue):
    """
    put recibe item y prioridad
    get devuelve item y prioridad
    
    item es un par ordenado que representa una arista
    """
    def __init__(self, G = None, from_list = False):
        PriorityQueue.__init__(self)
        self.counter = 0
        if not from_list and G:
            for node in G.getNodes():
                for neigh in G.getEdges(node):
                    #PriorityQueue.put(self, ((node, neigh), self.counter G.getWeight(node, neigh)))
                    PriorityQueue.put(self, ( (G.getWeight(node, neigh), self.counter, (node, neigh))))
        elif from_list:
            for edge in from_list:
                n1, n2, w = edge
                PriorityQueue.put(self, ( (w, self.counter, (n1, n2))))
                
    def __str__(self):
        return str(PriorityQueue)
    
    def put(self, item, priority):
        #print "putting" + str(item)
        PriorityQueue.put(self, (priority,  self.counter, item))
        self.counter += 1
        
    def get(self, *args, **kwargs):
        if PriorityQueue.empty(self):
            return False
        else:
            w, _, e = PriorityQueue.get(self, *args, **kwargs)
            return e, w