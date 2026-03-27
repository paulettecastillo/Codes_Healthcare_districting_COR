
import sys
import time
import pandas as pd
from collections import OrderedDict
import gurobipy as gp
from gurobipy import GRB
import numpy as np
import matplotlib.pyplot as plt
import random as rand
import math
import warnings
import os
import random
import ast
from PIL import Image, ImageDraw
import pytesseract
import itertools
import networkx as nx
from itertools import combinations
from itertools import chain
import copy


#-------------------------------------------Read Instance from TXT--------------------------------------------------------------------------------------
all_instancias= {}
with open(sys.argv[1], 'r') as archivo:
    count=0
    for linea in archivo:
        instancias = linea.strip().split('\t')
        all_instancias[count]=instancias
        count +=1

all_instancias = {k: v[0] for k, v in all_instancias.items()}

num_instancia= int(all_instancias[0])
instance= int(all_instancias[1])
uni = int(all_instancias[2])
pob = int(all_instancias[3])
recurso_h=ast.literal_eval(all_instancias[4])
recurso_c= ast.literal_eval(all_instancias[5])
MA= np.array(ast.literal_eval(all_instancias[6]))
poblacion= ast.literal_eval(all_instancias[7])
distancia= np.array(ast.literal_eval(all_instancias[9]))
tam_reg= float(all_instancias[10])



#---------------------------------------------------------Parameters--------------------------------------------------------------------------------------------------------------------------

#number of districts
dis= int(sys.argv[2])

#Set of Territorial units
V= np.array(range(uni)).tolist()
V1=[]
for i in V:
    V1.append(i)
V1.append('fict')

#Set of districts
K=np.array(range(dis)).tolist()

#We impose the parameter beta
beta= float(sys.argv[3])

#We form the limit distance for two territorial units that are in the same district
D=[]
for i in V:
    for j in V:
        if i<j:
            D.append(distancia[i][j])


DP= sum(D)/len(D)
DEP= (sum((D[i]-DP)**2 for i in range(len(D)))/len(D))**(1/2)
coef_l=DEP/DP
Lmax=math.ceil((tam_reg*3)/dis)


#EDGES
Eu_prima =[(i,j) for i in V for j in V if i < j if MA[i][j]==1 if distancia[i][j]<=Lmax]
Eu = Eu_prima + [('fict',j) for j in V]

#Arc
E= [(i,j) for i in V for j in V if i!=j if MA[i][j]==1 if distancia[i][j]<=Lmax]
EF = [(i,j) for i in V for j in V if i!=j if MA[i][j]==1 if distancia[i][j]<=Lmax] + [('fict',j) for j in V ]

PP= sum(poblacion[i] for i in V)/len(K)
PP1= sum(poblacion[i] for i in V)/len(V)

#We form the maximum desviation
alpha= (sum((poblacion[i]-PP1)**2 for i in V)/len(V))**(1/2)
coef=alpha/PP1

#Limits to territorial units in districts
s1=1
s2= 2*(len(V)/len(K))


no_vecinos={}
for i in V:
    no_vecinos[i]=[]

vecinos={}
for i in V:
    vecinos[i]=[]

#We compute the weight p-r for each territorial unit 
c=[0]* len(V)
for i in V:
    c[i]=((1-beta)*(poblacion[i]-recurso_c[i]))+(beta*(poblacion[i]-recurso_h[i]))


#We compute the degree for each territorial unit
degree={}
for i in V:
        degree[i]=0

for i in V:
    for j in V:
        if i!=j:
            if (i,j) in E:
                degree[i]= degree[i]+1

#We set the neighbors and no neighbors for each territorial unit
for i in V:
    for j in V:
        if (i,j) in E:
            vecinos[i].append(j) # vecinos de i

for i in V:
    for j in V:
        if distancia[i][j]>Lmax:
            no_vecinos[i].append(j)



#fot to form the subgraphs in the heuristic
adj = np.zeros((len(V),len(V)), dtype=int)
for (i, j) in E:
    adj[i][j] = 1

adyacencia=pd.DataFrame(adj)

primario=(sum(poblacion[i]-recurso_c[i] for i in V)/len(K))*(1-beta)
secundario=(sum(poblacion[i]-recurso_h[i] for i in V)/len(K))*beta
Lavg= primario + secundario

#For rescue the solution
Solution={}
etassc={}
etapsc={}
us={}
Capacity={}
Pod_d={}
Rec_d={}


























