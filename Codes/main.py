from models import*
from Read_Instance import *
import importlib
from functions import*

#--------------------------------

#Terminate
def root_node2(model, where):
    if where == GRB.Callback.MIPSOL:
        model.terminate()

#Function to create the model
def create_model(modelo,var,symmetry):

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

#Callback
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
#----------------------------------We start the resolution problems-------------------------------------------------------------
start_time = time.time()
#We solve the Mximum clique problem
m_clique= max_clique()

m_clique.update()
m_clique.optimize()


clique=[]
for i in V:
    if m_clique._x[i].x==1:
        clique.append(i)

#We solve te maximum Weighted clique problem
m_max_weight_clique= max_weighted_clique(clique)

m_max_weight_clique.update()
m_max_weight_clique.optimize()

#Rescue the Clique set 
lista_centros=[]
for i in V:
    if m_max_weight_clique._x[i].x==1:
        lista_centros.append(i)

#We reindex the nodes in the graph
mapping=reindex_nodes(V,lista_centros)
#print(mapping)


#Update all parameters
poblacion,recurso_c,recurso_h,distancia,E,EF,c,degree,vecinos,no_vecinos,adyacencia= reorder_nodes_after_clique(mapping)

import models
importlib.reload(models)
import functions
importlib.reload(functions)

end_time= time.time()
elapsed_time= end_time-start_time
#--------------------------We solve The model---------------------------------------------------------------------------------

var= int(sys.argv[4])
symmetry=int(sys.argv[5])
fixing=int(sys.argv[6])

m= create_model(sys.argv[7],var,symmetry)
tiempo_restante=3600-elapsed_time
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

m.update()
m.optimize(root_node_model)
lista_a,lista_f,lista_z,final_resuls, final_performance,elapsed_time = archivos(m,sys.argv[7],start_time,obj_bound_root_node,obj_value_root_node,best_Sol,best_nodes,best_time,symmetry,fixing,var)
