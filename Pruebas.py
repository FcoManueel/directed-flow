# -*- coding: utf-8 -*-
"""
Libreria de grafos
Autor: Francisco Manuel Valle Ruiz

Última actualizacion: Ford Fulkerson
"""
import random
from collections import deque


from mvr_graph import *
from mvr_shortest_path import *
from mvr_edge_queue import *
from mvr_utils import *
from mvr_algorithms import *
        
##########################################
##########################################
#####                                #####
#####        Recently added          #####
#####                                #####
##########################################
##########################################
def FordFulkerson(G,a,z):
    """
    <G> es una gráfica que cumple las caracteristicas de una
    red de transporte/flujo (dirigida, ponderada no negativa)
    Los 'pesos' de las aristas de G son las capacidades máximas

    <a> y <z> son (strings representando) fuente y sumidero
    respectivamente.
    """
    def getCapacity(G,n1,n2):
        return G.getWeight(n1,n2)
    def nodos_entrantes(G, n1):
        return [n for n in G if n1 in G.nodes[n]]

    def actualizar_flujo(G,F,tags,a,z,x=None):
        if x is None:
            x = z

        signo, k, _ = tags[x]
        if signo == '+':
            F[k,x] = F[k,x] + tags[z][2] # Revisar esta linea y la segunda siguiente: #ToCheck #ToDelete
        elif signo == '-':
            F[x,k] = F[x,k] - tags[z][2] #ToCheck #ToDelete
        
        if k == a:
            return True
        else:
            actualizar_flujo(G,F,tags,a,z,k)
            return False



    flujo_trivial = {(n,v): 0 for n in G for v in G.nodes[n]}
    F = flujo_trivial
    
    while(True):
        tags = {} # diccionario de 3-tuplas conteniendo ('+'|'-', nombre de antecesor, flujo recibido)
        tags[a] = ("+",a, float("inf"))
        already_check = []
        tagged = [a]

        counter = 0
        while counter < len(tagged): 
        # antes iteraba sobre los elementos de <tags>, pero como ocupo
        # mutar sus elementos terminé optando por llevar una lista 
        # (para conservar el orden) de los elementos que se van agregando, 
        # a tags e iterar sobre la longitud de dicha lista, así puedo agregar
        # tags sin problemas. Quizá esta medio cochino, pero it gets the work done
            j = tagged[counter]
            if j in already_check:
                counter +=1
                continue
            for i in G.nodes[j]:
                qji = getCapacity(G,j,i)
                fji = F[(j,i)]
                if i not in tags and fji < qji:
                    tags[i] = ('+', j ,min(tags[j][2], qji-fji))
                    tagged += i

            for i in nodos_entrantes(G,j):
                fij = F[(i,j)]
                if i not in tags and fij > 0:
                    tags[i] = ('-', j , min(tags[j][2], fij))
                    tagged += i
            
            # El nodo <j> se termino de examinar (todos sus vecinos tienen tag)
            already_check += j
            counter +=1
            
            if z in tags: # Se encontró una cadena aumentante
                actualizar_flujo(G,F,tags,a,z)
                break

        if z not in tags:
            return F
        
    assert True is False # Nunca se debería de llegar aquí. Algo está mal en el algoritmo.

##########################################
##########################################
#####                                #####
#####             Testing            #####
#####                                #####
##########################################
##########################################    
"""
G = Graph("El 'Irene Ponderado'", directed = True)
G.addNodes(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"])

G.addEdge("A","F", 2)
G.addEdge("A","G", 6)

G.addEdge("B","A", 1)
G.addEdge("B","C", 1)
G.addEdge("B","E", 4)

G.addEdge("D","B", 2)
G.addEdge("D","F", 1)

G.addEdge("E","C", 4)
G.addEdge("E","D", 2)
G.addEdge("E","G", 1)
G.addEdge("E","L", 4)

G.addEdge("F","E", 2)
G.addEdge("G","H", 3)
G.addEdge("H","I", 2)
G.addEdge("I","K", 10)

G.addEdge("J","G", 1)
G.addEdge("J","K", 1)
G.addEdge("J","M", 2)

G.addEdge("L","F", 2)
G.addEdge("L","G", 5)
G.addEdge("L","J", 3)

G.addEdge("M","L", 1)
#G.addEdge("G","G", None)  

print G

"""
G = Graph("La ciclo-negativa del desierto", directed = True)
G.addNodes(['A', 'B', 'C', 'D', 'E', 'F', 'G'])
G.addEdge("A","B", 1)
G.addEdge("A","F", 1)
G.addEdge("B","C", 2)
G.addEdge("C","D", 2)
G.addEdge("C","F", 3)
G.addEdge("D","E", 3)
G.addEdge("F","G", 4)
G.addEdge("G","C", 1)


print "------- Ford Fulkerson -------"
D = FordFulkerson(G, 'A', 'E')
print D
