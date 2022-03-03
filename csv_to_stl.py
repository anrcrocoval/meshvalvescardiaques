# -*- coding: utf-8 -*-
"""
Convertir un nuage de points csv en fichier stl

"""

import csv
from scipy.spatial import Delaunay
import matplotlib.tri
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
# import surf2stl
from stl import mesh

#lecture du fichier csv
# j'ai d'abord modifié le fichier csv en enlevant les tabulations avant le saut de ligne, et en remplaçant les autres tabulations par une virgule

file = open('resultline1.csv')
csvreader = csv.reader(file)
header = next(csvreader)
rows = []
for row in csvreader:
    rows.append(row)
file.close()



# 1er essai : maillage 3D du nuage de point qui renvoie donc un vecteur de tétrahèdres

string_points = np.array(rows)
points = string_points.astype(np.float64)
tri = Delaunay(points)


# mplot3d.axes3d.Axes3D.plot_trisurf(tri)

# ce plot ne fonctionne pas, apparamment tri n'est pas un object triangulation (surement car ce sont des tétrahèdres et non des trinagles)


# j'ai trouvé ce code sur internet pour obtenir le graphe du maillage tri

def plot_tri(ax, points, tri):
    edges = collect_edges(tri)
    x = np.array([])
    y = np.array([])
    z = np.array([])
    for (i,j) in edges:
        x = np.append(x, [points[i, 0], points[j, 0], np.nan])      
        y = np.append(y, [points[i, 1], points[j, 1], np.nan])      
        z = np.append(z, [points[i, 2], points[j, 2], np.nan])
    ax.plot3D(x, y, z, color='g', lw='0.1')

    ax.scatter(points[:,0], points[:,1], points[:,2], color='b')


def collect_edges(tri):
    edges = set()

    def sorted_tuple(a,b):
        return (a,b) if a < b else (b,a)
    # Add edges of tetrahedron (sorted so we don't add an edge twice, even if it comes in reverse order).
    for (i0, i1, i2, i3) in tri.simplices:
        edges.add(sorted_tuple(i0,i1))
        edges.add(sorted_tuple(i0,i2))
        edges.add(sorted_tuple(i0,i3))
        edges.add(sorted_tuple(i1,i2))
        edges.add(sorted_tuple(i1,i3))
        edges.add(sorted_tuple(i2,i3))
    return edges

fig = plt.figure()
ax = plt.axes(projection='3d')
plot_tri(ax, points, tri)

# le plot fonctionne, mais le maillage semble volumique avec des tétrahèdres, or on veut un maillage trinagulaire de la surface 3D



# 2eme essai : on essaie d'avoir un maillage triangulaire de la surface 3D du nuage de points

X, Y, Z = points[:,0], points[:,1], points[:,2]
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_trisurf(X, Y, Z, color='white', edgecolors='grey', alpha=0.5)
ax.scatter(X, Y, Z, c='red')
plt.show()


# import en stl

# surf2stl.write('mesh1.stl', X, Y, Z)

# ne fonctionne pas car il ne reconait pas le module surf2stl alors que je l'ai importé...

