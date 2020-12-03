# Import Statements
import numpy as np
# from tudatpy.kernel import constants
from tudatpy.kernel.interface import spice_interface
from tudatpy.kernel.simulation import environment_setup
from tudatpy.kernel.simulation import propagation_setup
from tudatpy.kernel.astro import conversion
from tudatpy.util import result2array

# Simulation Setup
spice_interface.load_standard_kernels()

simulation_start_epoch = 631108800.0
simulation_end_epoch = 631126800.0 #5 hours later


# Bodies
bodies_to_create = ["Earth","Sun"]

body_settings = environment_setup.get_default_body_settings(
    bodies_to_create,
    simulation_start_epoch,
    simulation_end_epoch,
    "Earth","J2000")

bodies = environment_setup.create_system_of_bodies(body_settings)


# Spacecraft

#CHESS 1
bodies.create_empty_body("CHESS1")

bodies.get_body("CHESS1").set_constant_mass(4.874)

reference_area_radiation = 0.1159
radiation_pressure_coefficient = 1.2
occulting_bodies = ["Earth"]
radiation_pressure_settings = environment_setup.radiation_pressure.cannonball(
    "Sun", reference_area_radiation, radiation_pressure_coefficient, occulting_bodies
)

environment_setup.add_radiation_pressure_interface(
            bodies, "CHESS1", radiation_pressure_settings )


#CHESS 2
bodies.create_empty_body("CHESS2")

bodies.get_body("CHESS2").set_constant_mass(4.874)

reference_area_radiation = 0.1159
radiation_pressure_coefficient = 1.2
occulting_bodies = ["Earth"]
radiation_pressure_settings = environment_setup.radiation_pressure.cannonball(
    "Sun", reference_area_radiation, radiation_pressure_coefficient, occulting_bodies
)

environment_setup.add_radiation_pressure_interface(
            bodies, "CHESS2", radiation_pressure_settings )


# Propagation Setup
bodies_to_propagate = ["CHESS1","CHESS2"]

central_bodies = ["Earth","Earth"]

# Acceleration Models
accelerations_settings_chess = dict(
    Sun=
    [
        propagation_setup.acceleration.cannonball_radiation_pressure()
    ],
    Earth=
    [
        propagation_setup.acceleration.spherical_harmonic_gravity(4,4)
    ]
    )

acceleration_settings = {"CHESS1": accelerations_settings_chess,
                         "CHESS2": accelerations_settings_chess}

acceleration_models = propagation_setup.create_acceleration_models(
    bodies,
    acceleration_settings,
    bodies_to_propagate,
    central_bodies)

# Initial System State
earth_gravitational_parameter = bodies.get_body("Earth").gravitational_parameter

initial_state_CHESS1 = conversion.keplerian_to_cartesian(
    gravitational_parameter = earth_gravitational_parameter,
    semi_major_axis = 6928136,
    eccentricity = 0.0,
    inclination = np.deg2rad(97.5926),
    argument_of_periapsis = np.deg2rad(0.0),
    longitude_of_ascending_node = np.deg2rad(90.0),
    true_anomaly = np.deg2rad(0.0)
)

initial_state_CHESS2 = conversion.keplerian_to_cartesian(
    gravitational_parameter = earth_gravitational_parameter,
    semi_major_axis = 7078136,
    eccentricity = 0.0424,
    inclination = np.deg2rad(97.5926),
    argument_of_periapsis = np.deg2rad(0.0),
    longitude_of_ascending_node = np.deg2rad(90.0),
    true_anomaly = np.deg2rad(0.0)
)

initial_state=np.hstack([initial_state_CHESS1,initial_state_CHESS2])

# Variables to Export
dependent_variables_to_save = [
    propagation_setup.dependent_variable.single_acceleration_norm(
        propagation_setup.acceleration.cannonball_radiation_pressure_type, "CHESS1", "Sun"
    ),
    propagation_setup.dependent_variable.single_acceleration_norm(
        propagation_setup.acceleration.cannonball_radiation_pressure_type, "CHESS2", "Sun"
    )
    ]

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

np.savetxt('2SCPropagationTest', result2array(dynamics_simulator.dependent_variable_history))



