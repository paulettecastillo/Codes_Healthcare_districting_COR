from models import*
from Read_Instance import *
import importlib
from fixing_variables import *

def root_node2(model, where):
    if where == GRB.Callback.MIPSOL:
        model.terminate()

def main(modelo,var,symmetry):
    m= model_a_z(var)
    
    if modelo=="DSF":
        m=DSF(m)

    if modelo=="MTZ":
        m=MTZ(m)
    
    if modelo=="MCF":
        m=MCF(m)
    
    if symmetry==1:
        m=Symmetry_Breaking(m)

    return m

def root_node_model(model, where):
        global obj_bound_root_node, obj_value_root_node,count_1,best_Sol,best_time,best_nodes
        if where == GRB.Callback.MIPNODE:
            if model.cbGet(GRB.Callback.MIPNODE_NODCNT) == 0 and count_1==0:
                count_1+=1
                obj_bound_root_node = model.cbGet(GRB.Callback.MIPNODE_OBJBND)  
                obj_value_root_node = model.cbGet(GRB.Callback.MIPNODE_OBJBST) 
        if where == GRB.Callback.MIPSOL:
            obj_val = model.cbGet(GRB.Callback.MIPSOL_OBJ)

            # Get the objective value of the new incumbent solution
            if best_Sol > model.cbGet(GRB.Callback.MIPSOL_OBJ) :
                end_time_1 = time.time()
                elapsed_time_1 = end_time_1 - start_time
                best_Sol =  model.cbGet(GRB.Callback.MIPSOL_OBJ)
                best_nodes = model.cbGet(GRB.Callback.MIPSOL_NODCNT)
                best_time = elapsed_time_1

def archivos(m,nombre_modelo,start_time,obj_bound_root_node,obj_value_root_node,best_Sol,best_nodes,best_time): 
    
    file_solucion = f"Solution_{nombre_modelo}_heu.txt"
    file_performance = f"Performance_{nombre_modelo}_heu.txt"
    #------------------------------------------------------- MODEL INFEASIBLE-------------------------------------------------------------------------------------------------------                     
    if m.status == GRB.Status.INFEASIBLE:
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
        FOBJ= m.ObjVal
        
        #time to solve model
        end_time = time.time()
        elapsed_time = end_time - start_time

        Best_UB = m.ObjVal
        Best_LB = m.ObjBound
        
        #Linear relaxation
        r1model = m.relax() 
        r1model.optimize() 
        m._relaxValue = r1model.ObjVal
        
        if Best_UB == 0:
            gap_int=100
        else:
            gap_int = 100*(Best_UB - m._relaxValue)/Best_UB
            
     
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
                str(best_time)+ '\t'+
                str(m._eta_psc.x) + '\t'+
                str(m._eta_ssc.x) + '\t'
                )

        f.close()
    
    return lista_a,lista_f,lista_z,file_solucion, file_performance,elapsed_time
   
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
    adj_new = np.zeros((len(V),len(V)), dtype=int)
    for (i, j) in E_cambio:
        adj_new[i][j] = 1

    adyacencia_new=pd.DataFrame(adj_new)

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

def archivos1(m,nombre_modelo,start_time_1,obj_bound_root_node,obj_value_root_node,best_Sol,best_nodes,best_time,nodos_fijos): 

    file_solucion = f"Solution_{nombre_modelo}_H.txt"
    file_performance = f"Performance_{nombre_modelo}_H.txt"
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
       
        FOBJ= m.ObjVal
        
        end_time = time.time()
        elapsed_time = end_time - start_time_1

        Best_UB = m.ObjVal
        Best_LB = m.ObjBound
        
        r1model = m.relax()
        r1model.optimize() 
        m._relaxValue = r1model.ObjVal
        
        if Best_UB == 0:
            gap_int=100
        else:
            gap_int = 100*(Best_UB - m._relaxValue)/Best_UB             
        
       
        gap_opt = m.MIPGap * 100
        print("GAP: {}%".format(gap_opt))
        print('GAP_opt',gap_opt)

        
        print('Best_UB',Best_UB)
        print('Best_lB',Best_LB)
        print('Relax_Value',m._relaxValue)
        
    #----------------------------------------------------------PRINTS SOLUCTION---------------------------------------------------------------------------------------------------------------------------------
        # for (i,j,k) in m._z.keys():
        #         if m._z[i,j,k].x >0.0003:
        #             print('z', (i,j,k), m._z[i,j,k].x)
                
        # for (i,k) in m._a.keys():
        #         if m._a[i,k].x >0.0003:
        #             print('a', (i,k), m._a[i,k].x)

        
        if nombre_modelo=='MTZ':

            Sum_pobd={}
            Sum_recd={}
            for i in range(len(K)):
                    Sum_pobd[i]= []
                    Sum_recd[i]= [] 

                 
            
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

            # for (i,j,q) in m._f.keys():
            #     if m._f[i,j,q].x >0.0003:
            #         print('f', (i,j,q), m._f[i,j,q].x)

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
                str(nodos_fijos) + '\t' +
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
   

def sol_simetrias(m,nombre_modelo,lista_a,lista_z,lista_f):

    solucion=lista_a
    solucion_z=lista_z
    solucion_f=lista_f
    
    for (i,q) in solucion:
        m._a[i,q].Start=solucion[i,q]
    
    for (i,j,q) in solucion_z:
        #print(i,q)
        m._z[i,j,q].Start=solucion_z[i,j,q]

    if nombre_modelo=='MTZ':
        for i in solucion_f:
            m._u[i].Start=solucion_f[i]

    if nombre_modelo=='MCF':
        
        for (i,j,k) in solucion_f:
            m._y[i,j,k].Start=solucion_f[i,j,k]


    if nombre_modelo=='DSF':
        
        for (i,j,q) in solucion_f:
            m._f[i,j,q].Start=solucion_f[i,j,q]
    
    
    return m

#----------------------------------We start the resolution problems-------------------------------------------------------------

start_time_1 = time.time()
#We solve the Mximum clique problem
m_clique= max_clique()

m_clique.update()
m_clique.optimize()

clique=[]

for i in V:
    if m_clique._x[i].x==1:
        clique.append(i)

m_max_weight_clique= max_weighted_clique(clique)

m_max_weight_clique.update()
m_max_weight_clique.optimize()

#Rescue the Clique set 
lista_centros=[]
for i in V:
    if m_max_weight_clique._x[i].x==1:
        lista_centros.append(i)

#Reindexation of the nodes
mapping=reindex_nodes(V,lista_centros)


#Update all parameters
poblacion,recurso_c,recurso_h,distancia,E,EF,c,degree,vecinos,no_vecinos,adyacencia= reorder_nodes_after_clique(mapping)

import models
importlib.reload(models)

import fixing_variables
importlib.reload(fixing_variables)
#------------------------------Heuristic-----------------------------------------------------------------------------

nodos_finales= nodos_posibles(lista_centros)
arcos=DFS(nodos_finales,lista_centros)


#--------------------------Partial solution to model-------------------------------------------------------------
m_heuristica= main(sys.argv[4],1,1)
obj_bound_root_node = None
obj_value_root_node = None
best_Sol = 10000000000000000000
best_time = None
best_nodes = None
count_1=0
end_time_1 = time.time()
elapsed_time_1=end_time_1 - start_time_1
tiempo_restante_1=3600-elapsed_time_1
start_time_2=time.time()
nombre_modelo=sys.argv[4]
#m_heuristica.setParam("OutputFlag", 0)
#m.setParam('MIPFocus', 1)  # Emphasize solution improvement
m_heuristica.setParam(GRB.Param.TimeLimit,360)


for q in arcos:
    for (i,j) in arcos[q]:
        m_heuristica.addConstr(m_heuristica._z[i,j,q]==1,name=f"constraint_z_{i,j},{q}")

for i in range(len(lista_centros)):
    m_heuristica.addConstr(m_heuristica._z['fict',i,i]==1,name=f"constraint_c_{i,i},{q}")


m_heuristica.update()
m_heuristica.optimize()

if m_heuristica.status == GRB.Status.INFEASIBLE:
    for q in arcos:
        for (i,j) in arcos[q]:
            constraint_name = f"constraint_z_{i,j},{q}"  # Dynamic name
            constr = m_heuristica.getConstrByName(constraint_name)  # Get the constraint object by name
            if constr:
                m_heuristica.remove(constr) 

    for i in range(len(lista_centros)):
        constraint_name = f"constraint_c_{i,i},{q}"  # Dynamic name
        constr = m_heuristica.getConstrByName(constraint_name)  # Get the constraint object by name
        if constr:
            m_heuristica.remove(constr) 

    check=1
    while check==1:
        check=0
        for i in nodos_finales:
            if len(nodos_finales[i]) > 1:
                nodos_finales[i].pop()
              
        arcos=DFS(nodos_finales,lista_centros)

        for q in arcos:
            for (i,j) in arcos[q]:
                m_heuristica.addConstr(m_heuristica._z[i,j,q]==1,name=f"constraint_z1_{i,j},{q}")

        for i in range(len(lista_centros)):
            m_heuristica.addConstr(m_heuristica._z['fict',i,i]==1,name=f"constraint_c1_{i,i},{q}")
        
        m_heuristica.update()
        m_heuristica.optimize()

        if m_heuristica.status == GRB.Status.INFEASIBLE:
            for q in arcos:
                for (i,j) in arcos[q]:
                    constraint_name = f"constraint_z1_{i,j},{q}"  # Dynamic name
                    constr = m_heuristica.getConstrByName(constraint_name)  # Get the constraint object by name
                    if constr:
                        m_heuristica.remove(constr) 

                for i in range(len(lista_centros)):
                    constraint_name = f"constraint_c1_{i,i},{q}"  # Dynamic name
                    constr = m_heuristica.getConstrByName(constraint_name)  # Get the constraint object by name
                    if constr:
                        m_heuristica.remove(constr) 
       
            check=1


        else:
            nodos_fijos= sum(len(lista) for lista in nodos_finales.values())
            lista_a,lista_f,lista_z,file_solucion, file_performance, elapsed_time =archivos1(m_heuristica,sys.argv[4],start_time_2,obj_bound_root_node,obj_value_root_node,best_Sol,best_nodes,best_time,nodos_fijos)
            check=0

else:   
    nodos_fijos= sum(len(lista) for lista in nodos_finales.values())     
    lista_a,lista_f,lista_z,file_solucion, file_performance,elapsed_time =archivos1(m_heuristica,sys.argv[4],start_time_2,obj_bound_root_node,obj_value_root_node,best_Sol,best_nodes,best_time,nodos_fijos)


#--------------------------We solve The model---------------------------------------------------------------------------------
var= int(sys.argv[5])
symmetry=int(sys.argv[6])
fixing=int(sys.argv[7])

m= main(sys.argv[8],var,symmetry)

nombre_modelo=sys.argv[8]
tiempo_restante= tiempo_restante_1-elapsed_time
start_time = time.time()
#m.setParam("OutputFlag", 0)
#m.setParam('MIPFocus', 1)  # Emphasize solution improvement
m.setParam(GRB.Param.TimeLimit,tiempo_restante)

#m.Params.LazyConstraints = 1
obj_bound_root_node = None
obj_value_root_node = None
best_Sol = 10000000000000000000
best_time = None
best_nodes = None
count_1=0

if fixing==1:
    for i in range(len(lista_centros)):
        m.addConstr(m._z['fict',i,i]==1)

m=sol_simetrias(m,sys.argv[8],lista_a,lista_z,lista_f)


m.update()
m.optimize(root_node_model)
lista_a,lista_f,lista_z,final_resuls, final_performance,elapsed_time = archivos(m,sys.argv[8],start_time,obj_bound_root_node,obj_value_root_node,best_Sol,best_nodes,best_time)
