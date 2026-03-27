from Read_Instance import *


#Max_clique
def max_clique():

    m = gp.Model()
    m._x= m.addVars(V, vtype=GRB.BINARY, lb = 0.0, ub=1.0)

    objetive = gp.quicksum(m._x[i] for i in V)
    m.setObjective(objetive, GRB.MAXIMIZE)

    for i in V:
        for j in V:
            if i!=j:
                if distancia[i][j]<=Lmax:
                    m.addConstr(m._x[i]+m._x[j]<=1)

    return m


#Max Weighted Clique
def max_weighted_clique(C):
    
    m = gp.Model()
    m._x= m.addVars(V, vtype=GRB.BINARY, lb = 0.0, ub=1.0)

    objetive = gp.quicksum(m._x[i]*c[i] for i in V)
    m.setObjective(objetive, GRB.MAXIMIZE)

    for i in V:
        for j in V:
            if i!=j:
                if distancia[i][j]<=Lmax:
                    m.addConstr(m._x[i]+m._x[j]<=1)

    m.addConstr(gp.quicksum(m._x[i] for i in V)==len(C))

    return m

#GROUP 2-3
def model_a_z(var):

    m = gp.Model()

    #VARIABLES

    if var==1:
        m._a= m.addVars(V,K,vtype=GRB.BINARY, lb=0, ub=1)
        m._z= m.addVars(EF,K,vtype=GRB.BINARY, lb = 0)

    if var==0:
        m._a= m.addVars(V,K,vtype=GRB.CONTINUOUS, lb=0, ub=1)
        m._z= m.addVars(EF,K,vtype=GRB.CONTINUOUS, lb=0, ub=1)

    m._eta_ssc = m.addVar(vtype=GRB.CONTINUOUS, lb = 0, ub = GRB.INFINITY)
    m._eta_psc = m.addVar(vtype=GRB.CONTINUOUS, lb =0, ub = GRB.INFINITY)

    #OBJECTIVE FUNCTION
    objetive = (1-beta)* m._eta_psc + beta* m._eta_ssc
    m.setObjective(objetive, GRB.MINIMIZE)

    #1
    for k in K:
        m.addConstr(gp.quicksum((poblacion[j]- recurso_h[j])*m._a[j,k] for j in V)<=m._eta_ssc)

    #2
    for k in K:
        m.addConstr(gp.quicksum((poblacion[j]- recurso_c[j])*m._a[j,k] for j in V)<=m._eta_psc)

    #3
    for j in V:
        m.addConstr(gp.quicksum(m._a[j,k] for k in K)==1)

    #4  Population homogeneity
    for q in K:
        m.addConstr(gp.quicksum(m._a[j,q]*poblacion[j] for j in V)>=PP*(1-coef))
        m.addConstr(gp.quicksum(m._a[j,q]*poblacion[j] for j in V)<=PP*(1+coef))
       
    #5 Compactness contraints
    for j in V:
        for i in V:
            for k in K:
                    if distancia[i][j]>Lmax:
                        m.addConstr(m._a[i,k]+m._a[j,k]<=1)

    #6 Number of territorial units per district
    for k in K:
        m.addConstr(gp.quicksum(m._a[j,k] for j in V)>= s1)
        m.addConstr(gp.quicksum(m._a[j,k] for j in V)<= s2)

    #7
    for q in K:
        m.addConstr(gp.quicksum(m._z['fict',j,q] for j in V)==1)

    #8
    for i in V:
        for k in K:
            m.addConstr(m._a[i,k]== gp.quicksum(m._z[j,i,k] for (j,ii) in EF if ii==i))
    #9
    for k in K:
        for j in V:
            m.addConstr(degree[j]*m._a[j,k]>= gp.quicksum(m._z[jj,i,k] for (jj,i) in EF if jj==j))

    #10
    for (i,j) in E:
        if i<j:
            if i!='fict':
                m.addConstr(gp.quicksum(m._z[i,j,q]+m._z[j,i,q] for q in K)<=1)

    return m

#Model MTZ
def MTZ(m):

    m._u=m.addVars(V1,vtype=GRB.CONTINUOUS, lb = 0)

    m.addConstr(m._u[0]==1)

    for (i,j) in EF:
        m.addConstr(m._u[j]>=m._u[i]+1+((len(V)-1)*(gp.quicksum(m._z[i,j,k] for k in K)-1)))

    return m

#Model DSF
def DSF(m):

    #VARIABLES
    m._f= m.addVars(EF,K,vtype=GRB.CONTINUOUS, lb = 0)


    #12
    for q in K:
        for (i,j) in EF:
                m.addConstr(m._f[i,j,q]<= len(V)*m._z[i,j,q])

    #10
    for q in K:
        m.addConstr(gp.quicksum(m._f['fict',i,q] for i in V)==gp.quicksum(m._a[i,q] for i in V))
    #11
    for i in V:
        for q in K:
            m.addConstr(gp.quicksum(m._f[j,ii,q] for (j,ii) in EF if ii==i)-gp.quicksum(m._f[ii,j,q] for (ii,j) in EF if ii==i)==m._a[i,q])


    return m

#Model MCF
def MCF(m):

    m._y= m.addVars(EF,V, vtype=GRB.CONTINUOUS, lb = 0, ub=1) 

    for (i,j) in EF:
        for k in V:
                m.addConstr(m._y[i,j,k]<=gp.quicksum(m._z[i,j,q] for q in K))

    #10
    for i in V:
        m.addConstr(gp.quicksum(m._y[u,j,i] for (u,j) in EF if u=='fict')==1)

    #11 
    for j in V:
        for k in V:
            if j!=k:
                m.addConstr(gp.quicksum(m._y[i,jj,k] for (i,jj) in EF if jj==j)- gp.quicksum(m._y[jj,i,k] for (jj,i) in EF if jj==j)==0)

    #5
    for k in V:
        m.addConstr(gp.quicksum(m._y[j,kk,kk] for (j,kk) in EF if k==kk)==1)

    return m

#Add Symmetry Breaking
def Symmetry_Breaking(m):

    for q in K:
         for i in V:
              for j in V:
                   if j<i:
                        m.addConstr(m._z['fict',i,q]+m._a[j,q]<=1)

    for q in K:
         for k in K:
              for i in V:
                   for j in V:
                        if i<j:
                             if k<q:
                                  m.addConstr(m._z['fict',i,q]+m._z['fict',j,k]<=1)

    for q in K:
        for i in V:
            for k in V:
                if (i,k) in E:
                    m.addConstr(m._a[i,q]+m._a[k,q]-gp.quicksum(m._a[j,q] for j in V if j<k if (i,j) in E)<= m._z[k,i,q]+m._z[i,k,q]+1)

    return m

