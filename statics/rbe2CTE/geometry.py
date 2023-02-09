import gmsh
import numpy as np
from pyNastran.bdf.bdf import BDF

def getPointClosest(gdf, refPoint):
    distances = np.linalg.norm(gdf['coords'] - refPoint, axis=1)
    min_index = np.argmin(distances)
    nodeId = gdf[min_index]['ID']
    return nodeId

gmsh.initialize()
gmsh.option.setNumber('General.Terminal', 1)
gmsh.option.setNumber('Mesh.MeshSizeFromPoints', 1)
model = gmsh.model
geom = gmsh.model.occ
model.add('bubble')

L = 1.0
gap = 0.2

geom.addPoint(0.0, 0.0, 0.0, tag=1)
geom.addPoint(L, 0.0, 0.0, tag=2)
geom.addPoint(L, L, 0.0, tag=3)
geom.addPoint(0.0, L, 0.0, tag=4)
lines1 = []
lines1.append(geom.addLine(1, 2,))
lines1.append(geom.addLine(2, 3,))
lines1.append(geom.addLine(3, 4,))
lines1.append(geom.addLine(4, 1,))

geom.addPoint(0.0, L/2, gap, tag=5)
geom.addPoint(L, L/2, gap, tag=6)
geom.addPoint(L, L/2, gap+L, tag=7)
geom.addPoint(0.0, L/2, gap+L, tag=8)
lines2 = []
lines2.append(geom.addLine(5, 6,))
lines2.append(geom.addLine(6, 7,))
lines2.append(geom.addLine(7, 8,))
lines2.append(geom.addLine(8, 5,))

curv1 = geom.addCurveLoop(lines1)
curv2 = geom.addCurveLoop(lines2)

surf1 = geom.addSurfaceFilling(curv1)
surf2 = geom.addSurfaceFilling(curv2)

geom.synchronize()

nNodes = 5

for line in geom.getEntities(1):
    gmsh.model.mesh.setTransfiniteCurve(line[1], nNodes)

gmsh.model.mesh.setTransfiniteSurface(surf1)
gmsh.model.mesh.setTransfiniteSurface(surf2)

gmsh.option.setNumber('Mesh.RecombineAll', 1)
gmsh.option.setNumber('Mesh.RecombinationAlgorithm', 1)
gmsh.option.setNumber('Mesh.Recombine3DLevel', 2)
gmsh.option.setNumber('Mesh.ElementOrder', 1)

geom.synchronize()
gmsh.model.mesh.generate(2)

# Generate the node array
nodes = gmsh.model.mesh.getNodes()
ids = nodes[0]
coords = nodes[1].reshape(-1,3)
dt = np.dtype([('ID', np.int32), ('coords', np.float32, (3,))])
gdf = np.zeros(len(nodes[0]), dtype=dt)
gdf['ID'] = ids
gdf['coords'] = coords

gmsh.model.addPhysicalGroup(2, [surf1,], 1, name="plate1")
gmsh.model.addPhysicalGroup(2, [surf2,], 2, name="plate2")

gmsh.write("geom.step")
gmsh.write("mesh.bdf")


bdf = BDF()
bdf.read_bdf('mesh.bdf', punch=True, xref=False)
E = 71e3
nu = 0.3
G = E/(2*(1+nu))
bdf.add_mat1(1, 71e3, G, nu, a =1.2e-5, tref=10.0)
bdf.add_pshell(1, mid1=1, t=1.0)
bdf.add_pshell(2, mid1=1, t=1.0)

# Loads
bdf.add_spc1(1, '123456', [1,2,3,4])


# Get point closest to (L, L/2, gap+(L/2))
refPoint = [L, L/2, gap+(L/2)]
nodeId1 = getPointClosest(gdf, [L, L/2, gap+(L/2)])
nodeId2 = getPointClosest(gdf, [0.0, L/2, gap+(L/2)])
bdf.add_spc1(1, '123456', [nodeId1, nodeId2])

# Get point closest to (L/2, L/2, L+gap)
force_node_id = getPointClosest(gdf, [L/2, L/2, L+gap])
bdf.add_force(force_node_id, 15, 100.0, [0, 0, 1.0])

# Temperature load
for nid in gdf['ID']:
    bdf.add_temp(100, {nid: 120.0})
#bdf.add_temp(100, {nid: 120.0 for nid in gdf['ID']}) 

bdf.punch=False
bdf.cross_reference()
bdf.sol = 101
bdf.create_subcases([1,2])

sub = bdf.subcases[0]
sub.add('ECHO', 'NONE',  [], 'STRING-type')

sub = bdf.subcases[1]
sub.add('SPC', 1, [], 'STRESS-type')
sub.add('LOAD', 10, [], 'STRESS-type')

sub = bdf.subcases[2]
sub.add('SPC', 1, [], 'STRESS-type')
sub.add('TEMPERATURE(LOAD)', 100, [], 'STRESS-type')

bdf.write_bdf('model.bdf')
                    



