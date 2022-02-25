# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 14:07:28 2022

@author: emile
"""


import pygeodesic.geodesic as geodesic
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.tri as mtri




""" On recrée un maillage """

filename = r'flat_triangular_mesh.txt'
result = geodesic.read_mesh_from_file(filename)
if result:
    points_bruts_tab, faces_brutes_tab = result

def liste(t):
    l = []
    for i in range(len(t)):
        tt = []
        for j in range(len(t[0])):
            tt.append(t[i, j])
        l.append(tt)
    return l

def tab(l):
    t = np.array(dtype=(len(l), len(l[0])))
    for i in range(len(t)):
        tt = []
        for j in range(len(t[0])):
            tt.append(t[i, j])
        l.append(tt)
    return l

points_bruts = liste(points_bruts_tab)
faces_brutes = liste(faces_brutes_tab)


def cond(x, y):
    if x <= 2.1:
        if x+y > 2.5:
            return False
        else:
            return True
    elif x < 2.9:
        if y > 0.4:
            return False
        else:
            return True
    else:
        if y > x-2.5 + 0.1:
            return False
        else:
            return True

tabBoolPoints = np.zeros(len(points_bruts))
tabBoolPoints = tabBoolPoints == 0

"""def decremFaces(faces_brutes, i):
    for j in range(len(faces_brutes)):
        a, b, c = faces_brutes[j]
        if a>i:
            a = a-1
        if b>i:
            b = b-1
        if c>i:
            c = c-1
        faces_brutes[j] = [a,b,c]
        if a==i or b==i or c==i:
            faces_brutes = faces_brutes[:j] + faces_brutes[j+1:]
        if j == len(faces_brutes)-1:
            break
    return faces_brutes"""

points = []
X, Y, Z = [], [], []
for i in range(len(points_bruts)):
    x, y, z = points_bruts[i]
    if cond(x, y):
        X.append(x)
        Y.append(y)
        Z.append(z)
        points.append([x, y, z])

#dist eucli entre les pts i et j
def norm(i, j, points): 
    x, y, z = points[i]
    xx, yy, zz = points[j]
    return np.sqrt((x-xx)**2 + (y-yy)**2 + (z-zz)**2)

#on crée maillage : on associe à chaque pt ses deux pts les plus proches -> donne une triangle
def creaMaille(points):
    faces = []
    
    for i in range(len(points)):
        dist = []
        for j in range(len(points)):
            dist.append(norm(i, j, points))
        dist[i] = 10*(dist[0]+1)
        m1 = min(dist)
        for l1 in range(len(dist)):
            if dist[l1] == m1:
                indiceMin1 = l1
                dist[l1] = 10*(dist[0]+1)
                break
        m2 = min(dist)
        for l2 in range(len(dist)):
            if dist[l2] == m2:
                indiceMin2 = l2
                dist[l2] = 10*(dist[0]+1)
                break
        m3 = min(dist)
        for l3 in range(len(dist)):
            if dist[l3] == m3:
                indiceMin3 = l3
                dist[l3] = 10*(dist[0]+1)
                break
        m4 = min(dist)
        for l4 in range(len(dist)):
            if dist[l4] == m4:
                indiceMin4 = l4
                break
        
        faces.append([i, indiceMin1, indiceMin2])
        faces.append([i, indiceMin2, indiceMin3])
        faces.append([i, indiceMin3, indiceMin4])
    
    return(faces)

faces = creaMaille(points)


points, faces = np.array(points), np.array(faces)









""" On définit le bord """

# True si le sommet est sur le bord d'étude, False sinon
def bord(S, eps=0.001):
    x, y, z = S
    if 0 <= x <= 2.1:
        return (abs(x+y-2.5) < eps)
    elif 2.1 < x <= 2.9:
        return (abs(y - 0.4) < eps)
    else:
        return (abs(y - (x-2.5)) < eps)
   
Xbord, Ybord, Zbord = [], [], []
for i in range(len(X)):
    if bord((X[i], Y[i], Z[i])):
        Xbord.append(X[i])
        Ybord.append(Y[i])
        Zbord.append(Z[i])

plt.scatter(X, Y)
triang = mtri.Triangulation(X, Y, faces)
plt.triplot(triang)
plt.scatter(Xbord, Ybord, c='red')
    






""" On calcule la distance géodésique de chaque point au bord """

source_indice = np.array([5])
geoalg = geodesic.PyGeodesicAlgorithmExact(points_bruts_tab, faces_brutes_tab)
distances, best_source = geoalg.geodesicDistances(source_indice)










""" IL FAUT TROUVER UN MEILLEUR MAILLAGE : PRENDRE LES 2 PTS LES PLUS PROCHES DE CHAQUE PT ! """
