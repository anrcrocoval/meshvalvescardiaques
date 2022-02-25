# -*- coding: utf-8 -*-
"""
On calcule la distance géodésique entre un point A et un point B

"""


import potpourri3d as pp
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pygeodesic.geodesic as geodesic




###############################################################################




# on traite donnée

def dejaPris(V, VV, i):
    j = 0
    trouve = False
    while j < len(VV) and not trouve:
        x, y, z = V[i]
        xx, yy, zz = VV[j]
        if (x==xx and y==yy and z==zz):
            trouve = True
        j += 1
    return trouve


# True si le sommet est sur le bord d'étude, False sinon
def bord(S, eps=0.001):
    x, y, z = S
    if 0 <= x <= 3:
        return (abs(-2/3*x+10 - y) <= eps)
    elif 3 < x <= 7:
        return (abs(y - 8) <= eps)
    else:
        return (abs(y - (2/3*x+10/3)) <= eps)
 
    
def suppDoublons(V):
    VV = []
    #X, Y, Z = [], [], []
    for i in range(len(V)):
        #x,y,z = V[i]
        #x = round(x, 5)
        #y = round(y, 5)
        #z = round(z, 5)
        if not dejaPris(V, VV, i):    
            #X.append(x)
            #Y.append(y)
            #Z.append(z)
            VV.append(V[i])
    return(np.array(VV))

def suppFaces(VV, F):
    n = len(VV)
    FF = np.array([[3*(n//3-1), 3*(n//3-1) + 1, 3*(n//3-1) + 2]])
    for i in range(n//3-1):
        FF = np.concatenate((FF, np.array([[3*i, 3*i+1, 3*i+2]])))
        FF = np.concatenate((FF, np.array([[3*i+1, 3*i+2, 3*i+3]])))
    return(FF)

# afficher les points en dégradé du 0 au 665  
def degrade(X, Y):
    #cm = plt.get_cmap("RdYlGn")
    col = np.arange(len(X))  
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(X, Y, s=20, c=col, marker='o')
    plt.show()
#degrade(X, Y) #--> répartition complètement aléatoire des points :(

# renvoie liste des bords et leur indice dans VV
def bordsTab(VV):
    bords = []
    for i in range(len(VV)):
        b = VV[i]
        if bord(b):
            bords.append([i, b])
    return bords
        
# renvoie la distance géodésique d'un point qcque au bord
def distBord(S, solver, bords):
    dist = solver.compute_distance(S) # dist entre S et ts les sommets
    #if S == 200:
    #    print(dist, len(dist))
    distMin = dist[bords[0][0]]
    for B in bords:
        i, b = B
        d = dist[i] # distance entre S et sommet i du bord
        if d < distMin:
            distMin = d 
    return distMin
#S = 63
#print("Distance entre S et bord : ", distBord(S, solver, bords))
            

# afficher des lignes de niveau en fonction des distances géodésiques
def lignesNiveau(VV, FF, nbNiveaux=10, ratioPlusGdeDist=1):
    solver = pp.PointCloudHeatSolver(VV)
    #solver = pp.MeshHeatMethodDistanceSolver(VV, FF)
    bords = bordsTab(VV) # il faudrait faire avec VV mais cela implique de changer F en FF
    dist = solver.compute_distance(bords[0][0])
    distMaxEntre2Points = max(dist) * ratioPlusGdeDist # valeur arbitraire
    X, Y, Z, couleurs = [], [], [], []
    
    for S in range(len(VV)):
        distanceAuBord = distBord(S, solver, bords)
        c = int(distanceAuBord / distMaxEntre2Points * nbNiveaux)
        couleurs.append(c)
        x, y, z = VV[S]
        X.append(x)
        Y.append(y)
        Z.append(z)

    # affichage graphique
    cmap = plt.cm.Spectral
    norm = plt.Normalize(vmin=0, vmax=nbNiveaux)
    plt.scatter(X, Y, s=30, c=cmap(norm(couleurs)))
    plt.show()
    
Vbrut, Fbrut = pp.read_mesh('maillage133.stl')
#VVV, FFF = geodesic.read_mesh_from_file('maillage133.stl')
#VV = suppDoublons(Vbrut)
#FF = suppFaces(VV, Fbrut)
lignesNiveau(Vbrut, Fbrut, nbNiveaux=25, ratioPlusGdeDist=1)

""" ESSAYER PYGEODESIC ?"""





















###############################################################################



"""


A = 0
B = 5


V, F = pp.read_mesh('line2.stl')
# V -> tableau de points avec 3 coo à chaque fois : les sommets
# F -> tableau des faces : chaque face est définie par les sommets qui la 
# constituent


# on connecte toutes les faces entre-elles : à améliorer
for sommet in F:
    x, y, z = sommet
    if x != len(V)-3:
        F = np.concatenate((F, np.array([[y, z, z+1]])))
    
    
# calcule la distance géodesique entre le point 7 et tous les autres points
solver = pp.MeshHeatMethodDistanceSolver(V, F)
dist = solver.compute_distance(A)

print('dist à A : ', dist)
#print('V = ', V)
print('F = ', F, len(F), '\n')

print("distance entre A et B : ", dist[B])
"""



###############################################################################








"""
# renvoie la liste des points qui forment le chemin géodésique le plus court
path_solver = pp.EdgeFlipGeodesicSolver(V,F) # shares precomputation for repeated solves
path_pts = path_solver.find_geodesic_path(v_start=2, v_end=3)

print('path_pts : ', path_pts)



###Cylindre.stl

V, F = pp.read_mesh('cylindre.stl')
F[3] = [1,3,4]
print("V = ", V)
print("\nF = ", F)
solver = pp.MeshHeatMethodDistanceSolver(V,F)
dist = solver.compute_distance(100)
print(dist)



# = Stateful solves
V, F = # a Nx3 numpy array of points and Mx3 array of triangle face indices
solver = pp3d.MeshVectorHeatSolver(V,F)

# Extend the value `0.` from vertex 12 and `1.` from vertex 17. Any vertex 
# geodesically closer to 12. will take the value 0., and vice versa 
# (plus some slight smoothing)
ext = solver.extend_scalar([12, 17], [0.,1.])

# Get the tangent frames which are used by the solver to define tangent data
# at each vertex
basisX, basisY, basisN = solver.get_tangent_frames()

# Parallel transport a vector along the surface
# (and map it to a vector in 3D)
sourceV = 22
ext = solver.transport_tangent_vector(sourceV, [6., 6.])
ext3D = ext[:,0,np.newaxis] * basisX +  ext[:,1,np.newaxis] * basisY

# Compute the logarithmic map
logmap = solver.compute_log_map(sourceV)
"""