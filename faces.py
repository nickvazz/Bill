import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
import random
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

verticies = []
prePerm = []
PHI = (1 + np.sqrt(5)) / 2
first3 = [(3*PHI,0,1), (1+2*PHI, PHI, 2), (2+PHI, 2*PHI, 1)]
xs = []; ys = []; zs = []; rho=[]; phi=[]; theta=[];

def permutations(vertex):
	(x,y,z) = vertex
	verticies.append((x,y,z))
	newX = y
	newY = z
	newZ = x
	verticies.append((newX, newY, newZ))
	newX2 = newY
	newY2 = newZ
	newZ2 = newX
	verticies.append((newX2, newY2, newZ2))
def perm8(vertex):
	(x,y,z) = vertex	
	if x != 0 and y != 0 and z != 0:
		prePerm.append((x, y, z))
		prePerm.append((x, y, -z))
		prePerm.append((x, -y, z))
		prePerm.append((x, -y, -z))
		prePerm.append((-x, y, z))
		prePerm.append((-x, y, -z))
		prePerm.append((-x, -y, z))
		prePerm.append((-x, -y, -z))
	else:
		prePerm.append((x, y, z))
		prePerm.append((x, y, -z))
		prePerm.append((-x, y, z))
		prePerm.append((-x, y, -z))
def distance(point1, point2):
	return np.sqrt((point2[0]-point1[0])**2 + (point2[1]-point1[1])**2 + (point2[2]-point1[2])**2)
def pltEdges(point1, point2):
	x1, y1, z1 = point1
	x2, y2, z2 = point2
	# ax.plot((x1,x2),(y1,y2),zs=(z1,z2))
def Pentagon(node):
	a,b,c,d,e = node
	new_pent_node = (verticies[a],verticies[b],verticies[c],verticies[d],verticies[e])
	return new_pent_node
def Hexagon(node):
	a,b,c,d,e,f = node
	new_pent_node = (verticies[a],verticies[b],verticies[c],verticies[d],verticies[e],verticies[f])
	return new_pent_node	
for i in range(3):
	perm8(first3[i])
for j in range(20):
	permutations(prePerm[j])
for i in range(60):
	xs.append(verticies[i][0])
	ys.append(verticies[i][1])
	zs.append(verticies[i][2])
for i in range(60):
	rho.append(np.sqrt(xs[i]**2 + ys[i]**2 + zs[i]**2))
	phi.append(np.arccos(xs[i]/np.sqrt(xs[i]**2 + ys[i]**2)))
	theta.append(np.arccos(zs[i] / np.sqrt(xs[i]**2 + ys[i]**2 + zs[i]**2)))

G=nx.Graph()
edges = []
for i in range(100000):
	a = random.randint(0,59)
	b = random.randint(0,59)	
	if distance(verticies[a],verticies[b]) == 2:
		edges.append((a,b))

edges = sorted(list(set(edges)))
faces = {}
for i in range(60): 
	faces[i] = []

for i in range(len(edges)):
	a,b = edges[i]
	point1 = verticies[edges[i][0]]
	point2 = verticies[edges[i][1]]
	# pltEdges(point1, point2)
	faces[edges[i][0]].append(edges[i][1])
	G.add_edge(a,b)

nx.draw_spectral(G,with_labels=True, edge_color=range(90), edge_cmap=plt.cm.cool)
plt.show()

pent_nodes = [
(9,27,55,58,33),
(0,12,37,40,18),
(6,24,43,46,30),
(1,13,38,41,19),
(7,25,44,47,31),
(10,34,59,56,28),
(45,42,26,8,32),
(4,16,50,53,22),
(5,23,51,48,17),
(2,14,36,39,20),
(3,15,49,52,21),
(11,29,54,57,35)
]
hex_nodes = [
(0,12,36,39,15,3),
(0,18,42,45,21,3),
(18,40,16,50,26,42),
(40,37,13,1,4,16),
(37,12,36,14,38,13),
(9,27,51,48,24,6),
(27,55,31,47,23,51),
(55,58,34,10,7,31),
(58,33,57,35,59,34),
(33,9,6,30,54,57),
(56,59,35,11,8,32),
(53,50,26,8,11,29),
(7,10,28,52,49,25),
(1,4,22,46,43,19),
(2,5,23,47,44,20),
(2,5,17,41,38,14),
(25,49,15,39,20,44),
(24,48,17,41,19,43),
(21,52,28,56,32,45),
(22,46,30,54,29,53)
]

pentagon_file = open('pentagon.txt', 'w')
hexagon_file = open('hexagon.txt', 'w')
pentagons_xyz = []
hexagons_xyz = []


for i in range(20):
	hexagons_xyz.append(Hexagon(hex_nodes[i]))

for j in range(12):
	pentagons_xyz.append(Pentagon(pent_nodes[j]))

for j in range(12):
	x=[];y=[];z=[]
	for i in range(5):
		x.append(pentagons_xyz[j][i][0])
		y.append(pentagons_xyz[j][i][1])
		z.append(pentagons_xyz[j][i][2])
		# ax.scatter(pentagons_xyz[j][i][0],pentagons_xyz[j][i][1],zs=[pentagons_xyz[j][i][2]])
	x.append(x[0])
	y.append(y[0])
	z.append(z[0])
	face = zip(x,y,z)
	face = str(face).replace("0,","0.001,")
	face = str(face).replace(", ",",")
	face = str(face).replace("[","")
	face = str(face).replace("]","")
	pentagon_file.write(str(face))
	if j < 11:
		pentagon_file.write('\n')
	# ax.plot(x,y,zs=z,zdir='z') 





for j in range(20):
	x=[];y=[];z=[]
	for i in range(6):
		x.append(hexagons_xyz[j][i][0])
		y.append(hexagons_xyz[j][i][1])
		z.append(hexagons_xyz[j][i][2])
		# ax.scatter(hexagons_xyz[j][i][0],hexagons_xyz[j][i][1],zs=[hexagons_xyz[j][i][2]])
	x.append(x[0])
	y.append(y[0])
	z.append(z[0])
	face = zip(x,y,z)
	face = str(face).replace("0,","0.001,")
	face = str(face).replace(", ",",")
	face = str(face).replace("[","")
	face = str(face).replace("]","")
	hexagon_file.write(str(face))
	if j < 19:
		hexagon_file.write('\n')
	# ax.plot(x,y,zs=z,zdir='z')

plt.show()








