# -*- coding: utf-8 -*-
"""
Implementación de algoritmos de ruta más corta
para la ibreria de grafos

Autor: Francisco Manuel Valle Ruiz

Última actualizacion: Floyd Warshall
"""
from mvr_graph import *
from mvr_edge_queue import *
from mvr_utils import *

####################################################
####################################################
###                                              ###
###           shortest path algorithms           ###
###                                              ###
####################################################
####################################################

def dijkstra_info(G, a, z):
    """
    @param G    Una grafica
    @param a    Un vertice inicial
    @param z    Un vertice final
    """
    print "Calculando la ruta mas corta entre ",a," y ",z
    etiquetas = {n: (n, float('inf')) for n in G.nodes}
    marcas = {}
    etiquetas[a] = (a, 0)
    marcas[a] = 'temp'

    def get_temporary_marks():
        return filter(lambda y: marcas[y] == 'temp', marcas.keys())

    def d_a(n):
        # Returns dist(a, n), where a is the inicial node in the algorithm 
        # and n is a previously marked node
        return etiquetas[n][1]
    
    def antecesor(n):
        return etiquetas[n][0]

    def elegir_vertice(marcas):
        return min(get_temporary_marks(), key= d_a)

    def mejor_ruta(n):
        ruta = [n]
        while ruta[0] != a:
            ruta.insert(0, antecesor(ruta[0]))
        return ruta

    def w(n1,n2):
        return G.getWeight(n1,n2)


    while(get_temporary_marks()):
        v = elegir_vertice(marcas)  # TODO, Devuelve el vértice v marcado temporalmente cuya d(a,v) sea menor (los desempates se dan por nomenclatura)
        marcas[v] = 'final'

        if v == z:
            return mejor_ruta(z), etiquetas
        for k in G.nodes[v]:
            if not marcas.has_key(k):
                marcas[k] = 'temp'
                etiquetas[k] = (v, d_a(v)+w(v,k))
            if marcas[k] == 'temp' and (d_a(v) + w(v,k) < d_a(k)):
                etiquetas[k] = (v, d_a(v) + w(v,k))
    
    print "No existe ruta de '",a,"'' a '",z,"'"
    return None

def dijkstra(G, a, z):
    path, _ = dijkstra_info(G, a, z)
    return path

def dijkstra_todos_info(G, a, debug = False):
    """
    @param G    Una grafica
    @param a    Un vertice inicial
    """
    etiquetas = {n: (n, float('inf')) for n in G.nodes}
    marcas = {}
    etiquetas[a] = (a, 0)
    marcas[a] = 'temp'

    def get_temporary_marks():
        return filter(lambda y: marcas[y] == 'temp', marcas.keys())
    
    def get_final_marks():
        return filter(lambda y: marcas[y] == 'final', marcas.keys())

    def d_a(n):
        # Returns dist(a, n), where a is the inicial node in the algorithm 
        # and n is a previously marked node
        return etiquetas[n][1]
    
    def antecesor(n):
        return etiquetas[n][0]

    def elegir_vertice(marcas):
        return min(get_temporary_marks(), key= d_a)

    def mejor_ruta(n):
        ruta = [n]
        while ruta[0] != a:
            ruta.insert(0, antecesor(ruta[0]))
        return ruta

    def w(n1,n2):
        return G.getWeight(n1,n2)


    while(len(G) != len(get_final_marks())):
        v = elegir_vertice(marcas)  # TODO, Devuelve el vértice v marcado temporalmente cuya d(a,v) sea menor (los desempates se dan por nomenclatura)
        
        if not v:
            for node in G:
                mejores_rutas.append(mejor_ruta(node))
            return (mejores_rutas, etiquetas)
        
        marcas[v] = 'final'
        for k in G.nodes[v]:
            if not marcas.has_key(k):
                marcas[k] = 'temp'
                etiquetas[k] = (v, d_a(v)+w(v,k))
            if marcas[k] == 'temp' and (d_a(v) + w(v,k) < d_a(k)):
                etiquetas[k] = (v, d_a(v) + w(v,k))
    #print "len(G) = ", len(G)
    #print "len(get_final_marks()) = ", len(get_final_marks())
    
    if len(G) != len(get_final_marks()):
        print "    --- ¡No se encontro arborecencia con raiz en ",a,"! ---"
        return None
    else:
        mejores_rutas = []
        for node in sorted(G.getNodes()):
            mejores_rutas.append(mejor_ruta(node))
        return (mejores_rutas, etiquetas)

def dijkstra_todos(G, a, debug = False):
    DT, _ = dijkstra_todos_info(G, a, debug)
    return DT

def dijkstra_general(G, a, debug = False):
    D, etiquetas = dijkstra_todos_info(G,a)

    def d_a(n):
        # Returns dist(a, n), where a is the inicial node in the algorithm 
        # and n is a previously marked node
        return etiquetas[n][1]
    
    def propagar(n, new_antecesor, change):
        if n:
            etiquetas[n] = (new_antecesor, d_a(n) + change)
            propagar(sucesor(n), n, change)
            
    def sucesor(n):
        sucesors = filter(lambda v: antecesor(v) == n,G.nodes[n].keys())
        if sucesors:
            return sucesors[0]
        else:
            return None


    def antecesor(n):
        return etiquetas[n][0]
    
    def mejor_ruta(n):
        ruta = [n]
        while ruta[0] != a:
            ruta.insert(0, antecesor(ruta[0]))
        return ruta

    def has_negative_cycle(n1,n2,w):
        current = n1
        cycle_node = n2
        cycle_nodes = [cycle_node]
        cycle_sum = w

        current = antecesor(current)
        while current != antecesor(current):
            if debug:
                print "current: ",current

            if current == cycle_node:
                cycle_nodes.append(n1)
                cycle_sum += G.getWeight(antecesor(n1), n1)
                return bool(cycle_sum <= 0)

            current = antecesor(current)
            cycle_nodes.append(current)
            cycle_sum += G.getWeight(current, sucesor(current))
        return False
    
    edges_not_in_D = [ (n1,n2,w) for (n1,n2,w) in G.getEdges() ]
    for (n1,n2,w) in G.getEdges():
        for sub_D in D:
            if (n1 in sub_D and
                n2 in sub_D and 
                sub_D.index(n1)+1 == sub_D.index(n2) and
                (n1,n2,w) in edges_not_in_D):
                    edges_not_in_D.remove((n1,n2,w))
    if debug:
        print D
        print edges_not_in_D

    edges_queue = EdgePriorityQueue(from_list= edges_not_in_D)
    
    while(not edges_queue.empty()):
        e, w = edges_queue.get()
        i, j = e
        new_length = d_a(i)+w
        antecesor_j = antecesor(j)
        if new_length < d_a(j) and not has_negative_cycle(i,j,w):
            propagar(j, sucesor(j), new_length - d_a(j))
            etiquetas[j] = (i, new_length)
            edges_queue.put((antecesor_j, j), G.getWeight(antecesor_j, j))
        elif has_negative_cycle(i,j,w):
            if debug:
                print "Se forman ciclos negativos baby. Regresando None..."
            return None
    mejores_rutas = []
    for node in sorted(G.getNodes()):
        mejores_rutas.append(mejor_ruta(node))
    return mejores_rutas

def floyd_warshall(G, debug = False):
    def tag2num(target, tags):
        for k, t in zip(tags.keys(), tags.values()):
            if t == target:
                return k
        return None

    def get_path(M,a,z,tags, debug=False):
        if debug:
            print "z: ",z
            print "tags: ",tags
        path = [tags[z]] + get_path_rec(M,a,z,tags)
        path.reverse()
        if debug:
            print path
        return path

    def get_path_rec(M,a,z,tags, debug=False):
        # returns a list with the name of the nodes
        # in' the shorthest path from a to z.
        # M is a matrix
        if debug:
            print "tags[z]: ",tags[z]
            print "z: ",z
        curr_tag = tags[z]  # current tag
        curr_i = z   # current index

        prev_tag = M[a][curr_i][0]
        prev_i = tag2num(prev_tag, tags)
        if debug:
            print "prev_tag: ", prev_tag
            print "prev_i: ", prev_i
        #while curr_i != prev_i:
        if prev_i == float("inf"):
            if debug:
                print "devolviendo None"
            return None
        elif prev_i == a:
            if debug:
                print "devolviendo [tags[a]]: ", [tags[a]]
            return [tags[a]]
        else:
            if debug:
                print "devolviendo [prev_tag] + get_path_rec(M, a, prev_i, tags)"
            return [prev_tag] + get_path_rec(M, a, prev_i, tags)


        
        previous_tag = tags[prev_i]
        if curr_tag == previous_tag:
            return [curr_tag]
        return [curr_tag] + get_path(M,a,previous,tags)

    def has_negative_cycles(M, tags):
        # M is a matrix
        # returns False if no negative cycles are found
        # else returns the first neg cycle it founds
        for z in xrange(len(M)):
            if M[z][z][1] < 0:
                return get_path(M,z,z,tags)
        return False

    size = len(G)
    matrix, tags = toMatrix(G)
    # Inicializar matrices
    for y in xrange(size):
        for x in xrange(size):
            matrix[y][x] = (tags[y], matrix[y][x])


    for k in xrange(size):
        for y in xrange(size):
            for x in xrange(size):
                if matrix[y][k][1]+matrix[k][x][1] < matrix[y][x][1]:
                    matrix[y][x] = (tags[k], matrix[y][k][1]+matrix[k][x][1])
                    
                if x == y and matrix[x][x][1] < 0:  # revisar existencia de ciclos negativos
                    print "Hay un ciclo negativo compuesto por: "
                    #print mprint(matrix)
                    print get_path(matrix,x,x,tags)
                    return None, None
                """
                if debug:
                    print "-- Iteracion k=",k," del algoritmo Floyd-Warshal --"
                    print "Revisando si el camino de tags[y]=",tags[y]," a tags[x]=",tags[x]
                    print "mejora si pasamos por tags[k]=",tags[k]
                    print "Los pesos son:"
                    print "     matrix[y][x]=",matrix[y][x]
                    print "       matrix[y][k]=",matrix[y][k]
                    print "       matrix[k][x]=",matrix[k][x]
                    print "     matrix[y][k] + matrix[k][x] = ",matrix[y][k]+matrix[k][x]
                    if matrix[y][x] != min(matrix[y][x], matrix[y][k]+matrix[k][x]):
                        print "Se mejora el minimo!\n\n"
                    else:
                        print "No hay mejora :/\n\n"
                """

    return (matrix, tags)