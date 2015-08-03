import glob
import numpy as np
import matplotlib.path as mpath
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from mpl_toolkits.mplot3d import Axes3D
from sympy import Plane, Point3D, Line3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

r = 6
images = glob.glob('*.png')

pentagon_file = open('pentagon.txt')
hexagon_file = open('hexagon.txt')
pentagons = []
hexagons = []

for line in pentagon_file:
	aline = line.split('\n')[0].split(',')
	for i in range(len(aline)):
		string = aline[i]
		if string[0] == '(':
			aline[i] = aline[i][1:]
		if string[-1] == ')':
			aline[i] = aline[i][:-1]
		aline[i] = float(aline[i])
	pentagons.append(aline)
for line in hexagon_file:
	aline = line.split('\n')[0].split(',')
	for i in range(len(aline)):
		string = aline[i]
		if string[0] == '(':
			aline[i] = aline[i][1:]
		if string[-1] == ')':
			aline[i] = aline[i][:-1]
		aline[i] = float(aline[i])
	hexagons.append(aline)

def distance(x,y,z):
	return np.sqrt(x**2 + y**2 + z**2)

angles_xyz = []
angles_PhiThetaRoll = []
for i in range(len(images)):
	(a,b,c) = images[i][7:-4].split('_')   # phi theta roll
	a = float(a)*np.pi/180.; b = float(b)*np.pi/180.; c = float(c)*np.pi/180.
	angles_PhiThetaRoll.append((a,b,c))
	x = r * np.cos(b) * np.sin(a)
	y = r * np.sin(b) * np.sin(a)
	z = r * np.cos(a)
	angles_xyz.append((x,y,z))

def plot_pentagons(plot_yes=True,specific_pentagons=False,pent_index=[]):
	pentagon_polygons = []
	if specific_pentagons == False:
		pent_nums = range(len(pentagons))
		pent_index = pent_nums
	elif specific_pentagons == True:
		pent_nums = pent_index
	for j in range(len(pentagons)):
		tempX = []
		tempY = []
		tempZ = []
		for i in range(0,18,3):
			tempX.append(pentagons[j][i])
		for i in range(1,18,3):
			tempY.append(pentagons[j][i])
		for i in range(2,18,3):
			tempZ.append(pentagons[j][i])
		if plot_yes == True:	
			for k in pent_index:
				if k == j:
					ax.plot(tempX,tempY,zs=tempZ,zdir='z')
		verts = []
		for i in range(5):
			verts.append((tempX[i],tempY[i],tempZ[i]))
		pentagon_polygons.append(np.asarray(verts))
	return pentagon_polygons

def plot_hexagons(plot_yes=True,specific_hexagons=False,hex_index=[]):
	hexagon_polygons = []
	if specific_hexagons == False:
		hex_nums = range(len(hexagons))
		hex_index = hex_nums
	elif specific_hexagons == True:
		hex_nums = hex_index
	for j in range(len(hexagons)):
		tempX = []
		tempY = []
		tempZ = []
		for i in range(0,21,3):
			tempX.append(hexagons[j][i])
		for i in range(1,21,3):
			tempY.append(hexagons[j][i])
		for i in range(2,21,3):
			tempZ.append(hexagons[j][i])
		if plot_yes == True:
			for k in hex_index:
				if k == j:
					ax.plot(tempX,tempY,zs=tempZ,zdir='z')
		verts = []
		for i in range(6):
			verts.append((tempX[i],tempY[i],tempZ[i]))
		hexagon_polygons.append(np.asarray(verts))
	return hexagon_polygons


# picture = 182320
picture = 12736
lineX = [0,-5]; lineY = [0,0]; lineZ = [0,-5]
lineX[1]=angles_xyz[picture][0]; lineY[1]=angles_xyz[picture][1]; lineZ[1]=angles_xyz[picture][2]
lineRho = distance(lineX[1],lineY[1],lineZ[1])

ax.plot(lineX,lineY,zs=lineZ)

hex_polygons = plot_hexagons(plot_yes=True,specific_hexagons=True,hex_index=[8])
pent_polygons = plot_pentagons(plot_yes=False,specific_pentagons=False,pent_index=[7])
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')
# plt.show()

line = (lineX[1], lineY[1], lineZ[1])

def projection(point,xyz):
	if xyz == 'x':
		new_point = (point[1], point[2])
	elif xyz == 'y':
		new_point = (point[0], point[2])
	elif xyz == 'z':
		new_point = (point[0], point[1])
	else:
		return 'projection error'
	return new_point

def create_path(list_of_points):
	Path = mpath.Path
	path_data = []
	for i in range(len(list_of_points)):
		if i == 0:
			temp = (Path.MOVETO, list_of_points[i])
		elif i == len(list_of_points) - 1:
			temp = (Path.CLOSEPOLY, list_of_points[i])
		else:
			temp = (Path.LINETO, list_of_points[i])
		path_data.append(temp)
	codes, verts = zip(*path_data)
	path = mpath.Path(verts, codes)

	return path

def check_projections(list_of_points, search_line):
	truth_projections = []
	for plane_proj in ['x', 'y', 'z']:
		new_list_of_points = []
		new_line = projection(search_line, plane_proj)

		for i in range(len(list_of_points)):
			new_list_of_points.append(projection(list_of_points[i], plane_proj))
		new_list_of_points = list(set(new_list_of_points))
		if len(list_of_points) == 5:
			path = create_path(new_list_of_points)
			check = path.contains_point(search_line)
		if len(list_of_points) == 6:
			path = create_path(new_list_of_points)
			check = path.contains_point(search_line)
		truth_projections.append(check)


		print '\n', plane_proj, check
		print path.vertices
		print plane_proj, check, '\n'

	return truth_projections

def find_bin(line):
	truth_cases = []
	for i in range(len(pent_polygons)):
		plane0 = Plane(Point3D(pent_polygons[i][0]), Point3D(pent_polygons[i][1]), Point3D(pent_polygons[i][2]))
		search_line = Line3D(Point3D(line), Point3D(0,0,0))
		plane_search_intersection = plane0.intersection(search_line)[0].evalf()

		point_plane_dist = plane0.distance(Point3D(line)).evalf()
		intersectionX = plane_search_intersection.x
		intersectionY = plane_search_intersection.y
		intersectionZ = plane_search_intersection.z
		intersection_line = (intersectionX, intersectionY, intersectionZ)

		print i
		true_or_false = check_projections(pent_polygons[i], intersection_line)
		print i

		for j in range(3):
			temp_string = 'xyz'
			if true_or_false[j] == 1:
				truth_cases.append((i,temp_string[j],point_plane_dist,'pent'))


	for i in range(len(hex_polygons)):
		plane0 = Plane(Point3D(hex_polygons[i][0]), Point3D(hex_polygons[i][1]), Point3D(hex_polygons[i][2]))
		search_line = Line3D(Point3D(line), Point3D(0,0,0))
		plane_search_intersection = plane0.intersection(search_line)[0].evalf()

		point_plane_dist = plane0.distance(Point3D(line)).evalf()
		intersectionX = plane_search_intersection.x
		intersectionY = plane_search_intersection.y
		intersectionZ = plane_search_intersection.z
		intersection_line = (intersectionX, intersectionY, intersectionZ)

		print i		
		true_or_false = check_projections(hex_polygons[i], intersection_line)
		print i

		for j in range(3):
			temp_string = 'xyz'
			if true_or_false[j] == 1:
				truth_cases.append((i,temp_string[j],point_plane_dist,'hex'))

	print truth_cases

find_bin(line)
plt.show()




















