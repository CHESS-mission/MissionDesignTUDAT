# Import Statements
import numpy as np
# from tudatpy.kernel import constants
from tudatpy.kernel.interface import spice_interface
from tudatpy.kernel.simulation import environment_setup
from tudatpy.kernel.simulation import propagation_setup
from tudatpy.kernel.astro import conversion
from tudatpy.util import result2array

# Choose RAAN values

number_RAAN=360 # defines the number of spacecraft, each with a different RAAN value in the initial state

RAAN=np.linspace(0,360,number_RAAN)

SC_NAMES=[]
for i in range(0,number_RAAN):
    SC_NAMES.append('CHESS'+str(RAAN[i])) # creates the name of each spacecraft
    


# Simulation Setup
spice_interface.load_standard_kernels()

simulation_start_epoch = 631108800.0
simulation_end_epoch = 631126800.0


# Bodies
bodies_to_create = ["Earth","Sun"]

body_settings = environment_setup.get_default_body_settings(
    bodies_to_create,
    simulation_start_epoch,
    simulation_end_epoch,
    "Earth","J2000")

bodies = environment_setup.create_system_of_bodies(body_settings)

reference_area_radiation = 0.1159
radiation_pressure_coefficient = 1.2

occulting_bodies = ["Earth"]
radiation_pressure_settings = environment_setup.radiation_pressure.cannonball(
    "Sun", reference_area_radiation, radiation_pressure_coefficient, occulting_bodies)

central_bodies=[]

bodies_to_propagate = SC_NAMES


accelerations_settings_chess = dict(
    Sun=[propagation_setup.acceleration.cannonball_radiation_pressure()],
    Earth=[propagation_setup.acceleration.spherical_harmonic_gravity(4,4)])

acceleration_settings ={}


earth_gravitational_parameter = bodies.get_body("Earth").gravitational_parameter

dependent_variables_to_save = []

for i in range(0,number_RAAN):
    bodies.create_empty_body(SC_NAMES[i])
    
    bodies.get_body(SC_NAMES[i]).set_constant_mass(4.874)
    
    environment_setup.add_radiation_pressure_interface(bodies,SC_NAMES[i],radiation_pressure_settings )
    
    central_bodies.append("Earth")
    
    acceleration_settings[SC_NAMES[i]]=accelerations_settings_chess
    
    initial_state_temp = conversion.keplerian_to_cartesian(
        gravitational_parameter = earth_gravitational_parameter,
        semi_major_axis = 7078136,
        eccentricity = 0.0424,
        inclination = np.deg2rad(97.5926),
        argument_of_periapsis = np.deg2rad(RAAN[i]),
        longitude_of_ascending_node = np.deg2rad(100.0),
        true_anomaly = np.deg2rad(0.0))
    if i==0:
        initial_state =initial_state_temp
    else:
        initial_state=np.hstack([initial_state,initial_state_temp])
    
    dependent_variables_to_save.append(propagation_setup.dependent_variable.single_acceleration_norm(
        propagation_setup.acceleration.cannonball_radiation_pressure_type, SC_NAMES[i], "Sun"))



acceleration_models = propagation_setup.create_acceleration_models(
    bodies,
    acceleration_settings,
    bodies_to_propagate,
    central_bodies)



# Propagator settings
propagator_settings = propagation_setup.propagator.translational(
    central_bodies,
    acceleration_models,
    bodies_to_propagate,
    initial_state,
    simulation_end_epoch,
    output_variables = dependent_variables_to_save
)

# Integrator settings
fixed_step_size = 10.0 #seconds

integrator_settings = propagation_setup.integrator.runge_kutta_4(
    simulation_start_epoch,
    fixed_step_size
)

# Create dynamics simulator
dynamics_simulator = propagation_setup.SingleArcDynamicsSimulator(
    bodies, integrator_settings, propagator_settings)

# Retrieve Results

np.savetxt('AOP_Optimisation_Results.dat', result2array(dynamics_simulator.dependent_variable_history))
np.savetxt('AOP_Optimisation_AOPValues.dat',RAAN)


