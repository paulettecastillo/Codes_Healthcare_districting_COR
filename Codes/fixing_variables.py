from Read_Instance import *


def nodos_posibles(lista_centros):

    nodos={}
    nodos_usados=[]
    for i in range(len(lista_centros)):
        nodos[i]=[]

    for i in range(len(lista_centros)):
        for j in V:
            if j !=i:
                if distancia[i][j]<=Lmax:
                    if j not in nodos_usados:
                        nodos[i].append(j)
        
        nodos[i].sort(key=lambda x: distancia[i][x])
        nodos[i].insert(0,i)

    nodos=dict(sorted(nodos.items(), key=lambda x: len(x[1])))

    for i in nodos:
        if len(nodos[i])>s2:
            nodos[i] = nodos[i][:int(s2)]
            
        #We and nodes until limit of population
        suma = 0
        suma_obj=0
        indice = 0
        while indice < len(nodos[i]):
            if suma + poblacion[nodos[i][indice]] <= PP*(1-coef):
                if suma_obj + c[nodos[i][indice]] <= Lavg:
                    
                    suma += poblacion[nodos[i][indice]]
                    suma_obj += c[nodos[i][indice]]
                    indice += 1
                else: 
                    del nodos[i][indice:]
                    break

            else:
                del nodos[i][indice:]
                break
        
        for n in nodos[i]:
            nodos_usados.append(n)
    
    return nodos

                                                                                                                                                                                               
def DFS(nodos_finales,lista_centros):
    
    tree={}

    for q in range(len(lista_centros)):
        lista_nodos = list(nodos_finales[q])
        nodos_validos = []
        nodos_validos.append(q)
        for j in lista_nodos:
            if j != q:
                vecinos = [i for i in lista_nodos if i != j and (j, i) in E]
                if len(vecinos) > 0:
                    nodos_validos.append(j)
                        
        asign= nodos_validos
        SubMA = adyacencia.loc[asign,asign]
        adj = {u: [v for v in asign if SubMA.at[u, v] != 0] for u in asign}

        visitado = set([asign[0]]) 
        spanning_tree = []
        pendientes = sorted([n for n in asign if n != asign[0]]) 

        while pendientes:
            nodo_agregado = False
            for i, v in enumerate(pendientes):  
                vecinos_visitados = [n for n in adj[v] if n in visitado]
               
                if vecinos_visitados: 
                    padre = min(vecinos_visitados) 
                    spanning_tree.append((padre, v))  
                    visitado.add(v) 
                    pendientes.pop(i)  
                    nodo_agregado=True
                    break  
            if not nodo_agregado:
                pendientes.clear() 
                break  

        tree[q] = spanning_tree
        tree[q].append(('fict', q)) 

    return tree

