import numpy as np
import os                   
import matplotlib.pyplot as plt 

import sharpy.utils.plotutils as pu        # Plotting utilities
from sharpy.utils.constants import deg2rad # Constant to conver degrees to radians

import sharpy.utils.generate_cases as gc

# Geometry
chord = 1.         # Chord of the wing
aspect_ratio = 16. # Ratio between lenght and chord: aspect_ratio = length/chord
wake_length = 50   # Length of the wake in chord lengths

# Discretization
num_node = 21           # Number of nodes in the structural discretisation
                        # The number of nodes will also define the aerodynamic panels in the
                        # spanwise direction
num_chord_panels = 4    # Number of aerodynamic panels in the chordwise direction
num_points_camber = 200 # The camber line of the wing will be defined by a series of (x,y)
                        # coordintes. Here, we define the size of the (x,y) vectors

# Structural properties of the beam cross section
mass_per_unit_length = 0.75 # Mass per unit length
mass_iner_x = 0.1           # Mass inertia around the local x axis
mass_iner_y = 0.05          # Mass inertia around the local y axis
mass_iner_z = 0.05          # Mass inertia around the local z axis
pos_cg_B = np.zeros((3))    # position of the centre of mass with respect to the elastic axis
EA = 1e7                    # Axial stiffness
GAy = 1e6                   # Shear stiffness in the local y axis
GAz = 1e6                   # Shear stiffness in the local z axis
GJ = 1e4                    # Torsional stiffness
EIy = 2e4                   # Bending stiffness around the flapwise direction
EIz = 5e6                   # Bending stiffness around the edgewise direction

# Operation
WSP = 2.                # Wind speed
air_density = 0.1       # Air density

# Time discretization
end_time = 5.0                  # End time of the simulation
dt = chord/num_chord_panels/WSP # Always keep one timestep per panel

aoa_ini_deg = 2.        # Angle of attack at the beginning of the simulation
aoa_end_deg = 1.        # Angle of attack at the end of the simulation

###############################################
# Structural Model
###############################################

wing = gc.AeroelasticInformation()
# Define the number of nodes and the number of nodes per element
wing.StructuralInformation.num_node = num_node
wing.StructuralInformation.num_node_elem = 3
# Compute the number of elements assuming basic connections
wing.StructuralInformation.compute_basic_num_elem()

# Generate an array with the location of the nodes
node_r = np.zeros((num_node, 3))
node_r[:,1] = np.linspace(0, chord*aspect_ratio, num_node)

wing.StructuralInformation.generate_uniform_beam(node_r,
                    mass_per_unit_length,
                    mass_iner_x,
                    mass_iner_y,
                    mass_iner_z,
                    pos_cg_B,
                    EA,
                    GAy,
                    GAz,
                    GJ,
                    EIy,
                    EIz,
                    num_node_elem = wing.StructuralInformation.num_node_elem,
                    y_BFoR = 'x_AFoR',
                    num_lumped_mass=0)


wing.StructuralInformation.boundary_conditions[0] = 1
wing.StructuralInformation.boundary_conditions[-1] = -1

###############################################
# Aerodynamics Model
###############################################

# Compute the number of panels in the wake (streamwise direction) based on the previous paramete
wake_panels = int(wake_length*chord/dt)

# Define the coordinates of the camber line of the wing
wing_camber = np.zeros((1, num_points_camber, 2))
wing_camber[0, :, 0] = np.linspace(0, 1, num_points_camber)

# Generate blade aerodynamics
wing.AerodynamicInformation.create_one_uniform_aerodynamics(wing.StructuralInformation,
                                 chord = chord,
                                 twist = 0.,
                                 sweep = 0.,
                                 num_chord_panels = num_chord_panels,
                                 m_distribution = 'uniform',
                                 elastic_axis = 0.5,
                                 num_points_camber = num_points_camber,
                                 airfoil = wing_camber)


###############################################
# Simulation Model
###############################################

# Gather data about available solvers
SimInfo = gc.SimulationInformation() # Initialises the SimulationInformation class
SimInfo.set_default_values()         # Assigns the default values to all the solvers

SimInfo.solvers['BeamLoader']

SimInfo.solvers['SHARPy']['flow'] = ['BeamLoader',
                        'AerogridLoader']

SimInfo.solvers['SHARPy']['case'] = 'plot'
SimInfo.solvers['SHARPy']['route'] = './'
SimInfo.solvers['SHARPy']['write_screen'] = 'off'

SimInfo.solvers['AerogridLoader']['unsteady'] = 'on'
SimInfo.solvers['AerogridLoader']['mstar'] = wake_panels
SimInfo.solvers['AerogridLoader']['freestream_dir'] = np.array([1.,0.,0.])
SimInfo.solvers['AerogridLoader']['wake_shape_generator'] = 'StraightWake'

direction = np.array([np.cos(aoa_ini_deg*deg2rad), 0., np.sin(aoa_ini_deg*deg2rad)]), 
SimInfo.solvers['AerogridLoader']['wake_shape_generator_input'] =  \
                {'u_inf': WSP, 'u_inf_direction': direction, 'dt': dt}


gc.clean_test_files(SimInfo.solvers['SHARPy']['route'], SimInfo.solvers['SHARPy']['case'])
wing.generate_h5_files(SimInfo.solvers['SHARPy']['route'], SimInfo.solvers['SHARPy']['case'])
SimInfo.generate_solver_file()


