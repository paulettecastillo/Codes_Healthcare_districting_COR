from Read_Instance import *


#Function to rescue the solution and performance.
def archivos(m,nombre_modelo,start_time,obj_bound_root_node,obj_value_root_node,best_Sol,best_nodes,best_time,symmetry,fixing,var): 
    #Recopilamos poblacion y recursos por distrito
    if symmetry==0 and fixing==1:
        file_solucion = f"Solution_{nombre_modelo}_F.txt"
        file_performance = f"Performance_{nombre_modelo}_F.txt"
    if symmetry==1 and fixing==0:
        file_solucion = f"Solution_{nombre_modelo}_S.txt"
        file_performance = f"Performance_{nombre_modelo}_S.txt"

    if symmetry==1 and fixing==1:
        file_solucion = f"Solution_{nombre_modelo}_S_F.txt"
        file_performance = f"Performance_{nombre_modelo}_S_F.txt"
    #------------------------------------------------------- MODEL INFEASIBLE-------------------------------------------------------------------------------------------------------                     
    if m.status == GRB.Status.INFEASIBLE:
        print("EL modelo es infactible")

        f = open(file_solucion, 'a')        
        f.write('\n' +
                str(num_instancia)+ '\t' +
                str(instance)+ '\t' +
                str(dis) + '\t' +
                str(uni) + '\t' +
                str(beta) + '\t' +
                str("Infeasible") + '\t'                            
                )
        f.close()
        
        f = open(file_performance, 'a')
        f.write('\n' +
                str(num_instancia)+ '\t' +
                str(instance) + '\t' +
                str(dis) + '\t' +
                str(uni) + '\t' +
                str(beta) + '\t' +
                str("Infeasible") + '\t' 
                )

        f.close()
#--------------------------------------------------------FEASIBLE------------------------------------------------------------------------------------------------------------------------------
    else: 
        # print("El modelo es factible")
        FOBJ= m.ObjVal
        
        #time to solve model
        end_time = time.time()
        elapsed_time = end_time - start_time

        #gap de optimalidad
        Best_UB = m.ObjVal
        Best_LB = m.ObjBound
        
        
        #RELAJACIÓN LINEAL
        r1model = m.relax() #relajacion lineal del modelo
        r1model.optimize() #optimizar la relajacion lineal
        m._relaxValue = r1model.ObjVal
        
        if Best_UB == 0:
            gap_int=100
        else:
            gap_int = 100*(Best_UB - m._relaxValue)/Best_UB

        if var==0:
            gap_opt='-'              
        
        else:
            gap_opt = m.MIPGap * 100
            print("GAP: {}%".format(gap_opt))
            print('GAP_opt',gap_opt)

        
        print('Best_UB',Best_UB)
        print('Best_lB',Best_LB)
        print('Relax_Value',m._relaxValue)
        
#----------------------------------------------------------PRINTS SOLUCTION---------------------------------------------------------------------------------------------------------------------------------
        for (i,j,k) in m._z.keys():
                if m._z[i,j,k].x >0.0003:
                    print('z', (i,j,k), m._z[i,j,k].x)
        
        if nombre_modelo=='MTZ':

            Sum_pobd={}
            Sum_recd={}
            for i in range(len(K)):
                    Sum_pobd[i]= []
                    Sum_recd[i]= [] 

            for i in m._u.keys():
                if m._u[i].x >0.0003:
                    print('u',i, m._u[i].x)
            
            lista_f={}
            for i in m._u.keys():
                lista_f[i]= m._u[i].x

            lista_a={}
            for (i,k) in m._a.keys():
                lista_a[i,k]= m._a[i,k].x

            lista_z={}
            for (i,k,q) in m._z.keys():
                lista_z[i,k,q]= m._z[i,k,q].x

            for (i,k) in m._a.keys():
                if m._a[i,k].x >0.0003:
                    Sum_pobd[k].append(poblacion[i])
                    Sum_recd[k].append(recurso_c[i]) 
            
            Solution[dis, beta] = [(i, j, k) for k in K for (i,j) in EF if m._z[i, j, k].x > 0.1]
            Capacity[dis]= [(sum(Sum_pobd[k][i] for i in range(len(Sum_pobd[k])))-sum(Sum_recd[k][i] for i in range(len(Sum_recd[k])))) for k in K]
            Pod_d[dis]=  [sum(Sum_pobd[k][i] for i in range(len(Sum_pobd[k])))for k in K]
            Rec_d[dis]= [sum(Sum_recd[k][i] for i in range(len(Sum_recd[k]))) for k in K]

                    
        if nombre_modelo=='MCF':

            Sum_pobd={}
            Sum_recd={}
            for i in range(len(K)):
                    Sum_pobd[i]= []
                    Sum_recd[i]= [] 

            for (i,j,k) in m._y.keys():
                if m._y[i,j,k].x >0.0003:
                    print('y', (i,j,k), m._y[i,j,k].x)
            
            lista_f={}
            for (i,k,q) in m._y.keys():
                lista_f[i,k,q]= m._y[i,k,q].x
            
            lista_a={}
            for (i,k) in m._a.keys():
                lista_a[i,k]= m._a[i,k].x

            lista_z={}
            for (i,k,q) in m._z.keys():
                lista_z[i,k,q]= m._z[i,k,q].x
            
            for (i,k) in m._a.keys():
                if m._a[i,k].x >0.0003:
                    Sum_pobd[k].append(poblacion[i])
                    Sum_recd[k].append(recurso_c[i]) 
                
            Solution[dis, beta] = [(i, j, k) for k in K for (i,j) in EF if m._z[i, j, k].x > 0.1]
            Capacity[dis]= [(sum(Sum_pobd[k][i] for i in range(len(Sum_pobd[k])))-sum(Sum_recd[k][i] for i in range(len(Sum_recd[k])))) for k in K]
            Pod_d[dis]=  [sum(Sum_pobd[k][i] for i in range(len(Sum_pobd[k])))for k in K]
            Rec_d[dis]= [sum(Sum_recd[k][i] for i in range(len(Sum_recd[k]))) for k in K]

        
        if nombre_modelo=='DSF':

            Sum_pobd={}
            Sum_recd={}
            for i in range(len(K)):
                    Sum_pobd[i]= []
                    Sum_recd[i]= [] 

            lista_f={}
            for (i,k,q) in m._f.keys():
                lista_f[i,k,q]= m._f[i,k,q].x


            lista_a={}
            for (i,k) in m._a.keys():
                lista_a[i,k]= m._a[i,k].x

            lista_z={}
            for (i,k,q) in m._z.keys():
                lista_z[i,k,q]= m._z[i,k,q].x
            

            for (i,k) in m._a.keys():
                if m._a[i,k].x >0.0003:
                    Sum_pobd[k].append(poblacion[i])
                    Sum_recd[k].append(recurso_c[i]) 
            
            Solution[dis, beta] = [(i, j, k) for k in K for (i,j) in EF if m._z[i, j, k].x > 0.1]
            Capacity[dis]= [(sum(Sum_pobd[k][i] for i in range(len(Sum_pobd[k])))-sum(Sum_recd[k][i] for i in range(len(Sum_recd[k])))) for k in K]
            Pod_d[dis]=  [sum(Sum_pobd[k][i] for i in range(len(Sum_pobd[k])))for k in K]
            Rec_d[dis]= [sum(Sum_recd[k][i] for i in range(len(Sum_recd[k]))) for k in K]

 #----------------------------------RESCUED THE SOLUTION------------------------------------------------------------------------------------------------------------------------

        
        
        f = open(file_solucion, 'a')
        
        f.write('\n' +
                str(num_instancia)+ '\t' +
                str(instance)+ '\t' +
                str(dis) + '\t' +
                str(uni) + '\t' +
                str(beta) + '\t' +
                str(Solution[dis, beta]) + '\t'+
                str(Capacity[dis]) + '\t'+
                str(Pod_d[dis]) + '\t'+
                str(Rec_d[dis]) + '\t'+
                # str(m._eta_psc.x) + '\t'+
                # str(m._eta_ssc.x) + '\t'+
                str(degree) + '\t'
                )

        f.close()
        
        f = open(file_performance, 'a')

        f.write('\n' +
                str(num_instancia)+ '\t' +
                str(instance) + '\t' +
                str(dis) + '\t' +
                str(uni) + '\t' +
                str(beta) + '\t' +
                str(m.objVal) + '\t' +
                str(m.ObjBound) + '\t' +
                str(gap_opt) + '\t' +
                str(m._relaxValue) + '\t'+
                str(gap_int) +'\t'+
                str(elapsed_time) + '\t'+
                str(m.NodeCount) + '\t'+
                str(obj_bound_root_node) + '\t'+
                str(obj_value_root_node) + '\t'+
                str(best_Sol) + '\t'+
                str(best_nodes)+ '\t'+
                str(best_time)+ '\t'
                )

        f.close()
    
    return lista_a,lista_f,lista_z,file_solucion, file_performance,elapsed_time

#Function to reindex the nodes
def reorder_nodes_after_clique(mapping):

    E_new = set()
    for edge in E:
        if isinstance(edge, (list, tuple)) and len(edge) == 2:
            i, j = edge
            new_i = mapping[i]
            new_j = mapping[j]
            E_new.add((min(new_i, new_j), max(new_i, new_j)))

        else:
            print(f"Advertencia: Arco con formato inválido: {edge}")


    nodos_originales = list(range(distancia.shape[0]))
    n_nuevos = len(set(mapping.values()))
    

    nueva_matriz_distancia = np.zeros((n_nuevos, n_nuevos))

    for viejo_i in nodos_originales:
        if viejo_i in mapping:
            nuevo_i = mapping[viejo_i]
            for viejo_j in nodos_originales:
                if viejo_j in mapping:
                    nuevo_j = mapping[viejo_j]
                    nueva_matriz_distancia[nuevo_i][nuevo_j] = distancia[viejo_i][viejo_j]


    # Determinar el tamaño de la nueva lista
    max_nuevo_nodo = max(mapping.values())
    nueva_lista_poblacion = [0] * (max_nuevo_nodo+1)

    # Reordenar según el mapeo
    for nodo_original, nodo_nuevo in mapping.items():
        if nodo_original < len(poblacion):
            nueva_lista_poblacion[nodo_nuevo] = poblacion[nodo_original]


    nueva_lista_rc = [0] * len(V)

    # Reordenar según el mapeo
    for nodo_original, nodo_nuevo in mapping.items():
        nueva_lista_rc[nodo_nuevo] = recurso_c[nodo_original]

    nueva_lista_rh = [0] * len(V)

    for nodo_original, nodo_nuevo in mapping.items():
        nueva_lista_rh[nodo_nuevo] = recurso_h[nodo_original]


    E_new=list(E_new)

    E_final=[]

    for (i,j) in E_new:
        E_final.append((i,j))
        E_final.append((j,i))

    E_cambio=E_final

    EF_cambio=E_cambio+ [('fict',j) for j in V ]

    #Update the weights

    c_new=[0]* len(V)
    for i in V:
        c_new[i]=((1-beta)*(nueva_lista_poblacion[i]-nueva_lista_rc[i]))+(beta*(nueva_lista_poblacion[i]-nueva_lista_rh[i]))

    degree_new={}
    for i in V:
            degree_new[i]=0

    for i in V:
        for j in V:
            if i!=j:
                if (i,j) in E_cambio:
                    degree_new[i]= degree_new[i]+1


    no_vecinos_new={}
    for i in V:
        no_vecinos_new[i]=[]

    vecinos_new={}
    for i in V:
        vecinos_new[i]=[]

    for i in V:
        for j in V:
            if (i,j) in E_cambio:
                vecinos_new[i].append(j) # vecinos de i

    for i in V:
        for j in V:
            if nueva_matriz_distancia[i][j]>Lmax:
                no_vecinos_new[i].append(j)

    #fot to form the subgraphs in the heuristic
    adj = np.zeros((len(V),len(V)), dtype=int)
    for (i, j) in E_cambio:
        adj[i][j] = 1

    adyacencia_new=pd.DataFrame(adj)

    # Actualizar Read_Instance directamente
    import Read_Instance as RI
    RI.poblacion = nueva_lista_poblacion
    RI.recurso_c = nueva_lista_rc
    RI.recurso_h = nueva_lista_rh
    RI.distancia = nueva_matriz_distancia
    RI.E = E_cambio
    RI.EF = EF_cambio
    RI.c = c_new
    RI.degree = degree_new
    RI.vecinos = vecinos_new
    RI.no_vecinos = no_vecinos_new
    RI.adyacencia = adyacencia_new


    return nueva_lista_poblacion,nueva_lista_rc,nueva_lista_rh,nueva_matriz_distancia,E_cambio,EF_cambio,c_new,degree_new,vecinos_new,no_vecinos_new,adyacencia_new

def reindex_nodes(all_nodes, selected_nodes):
    selected_nodes = sorted(selected_nodes)
    other_nodes = [n for n in all_nodes if n not in selected_nodes]

    new_order = selected_nodes + other_nodes
    index_map = {old: new for new, old in enumerate(new_order)}

    return index_map
