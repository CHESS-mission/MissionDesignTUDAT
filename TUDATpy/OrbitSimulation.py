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
simulation_end_epoch = 638971199.0


# Bodies
bodies_to_create = ["Earth","Moon","Sun","Jupiter"]

body_settings = environment_setup.get_default_body_settings(
    bodies_to_create,
    simulation_start_epoch,
    simulation_end_epoch,
    "Earth","J2000")

bodies = environment_setup.create_system_of_bodies(body_settings)


# Spacecraft

#CHESS 1
bodies.create_empty_body("CHESS1")

bodies.get_body("CHESS1").set_constant_mass(4.0)

reference_area_radiation = 0.09
radiation_pressure_coefficient = 1.2
occulting_bodies = ["Earth"]
radiation_pressure_settings = environment_setup.radiation_pressure.cannonball(
    "Sun", reference_area_radiation, radiation_pressure_coefficient, occulting_bodies
)

environment_setup.add_radiation_pressure_interface(
            bodies, "CHESS1", radiation_pressure_settings )

drag_coefficient = 1.5
reference_area_drag_1 = 0.09

aero_coefficient_settings_1 = environment_setup.aerodynamic_coefficients.constant(
    reference_area_drag_1,[drag_coefficient,0,0],
    are_coefficients_in_aerodynamic_frame=True,
    are_coefficients_in_negative_axis_direction=True
)

environment_setup.add_aerodynamic_coefficient_interface(
            bodies, "CHESS1", aero_coefficient_settings_1)

#CHESS 2
bodies.create_empty_body("CHESS2")

bodies.get_body("CHESS2").set_constant_mass(4.0)

reference_area_radiation = 0.09
radiation_pressure_coefficient = 1.2
occulting_bodies = ["Earth"]
radiation_pressure_settings = environment_setup.radiation_pressure.cannonball(
    "Sun", reference_area_radiation, radiation_pressure_coefficient, occulting_bodies
)

environment_setup.add_radiation_pressure_interface(
            bodies, "CHESS2", radiation_pressure_settings )

drag_coefficient = 1.5
reference_area_drag_2 = 0.09

aero_coefficient_settings_2 = environment_setup.aerodynamic_coefficients.constant(
    reference_area_drag_2,[drag_coefficient,0,0],
    are_coefficients_in_aerodynamic_frame=True,
    are_coefficients_in_negative_axis_direction=True
)

environment_setup.add_aerodynamic_coefficient_interface(
            bodies, "CHESS2", aero_coefficient_settings_2 )


# Propagation Setup
bodies_to_propagate = ["CHESS1","CHESS2"]

central_bodies = ["Earth","Earth"]

# Acceleration Models
accelerations_settings_chess = dict(
    Sun=
    [
        propagation_setup.acceleration.cannonball_radiation_pressure(),
        propagation_setup.acceleration.point_mass_gravity()
    ],
    Earth=
    [
        propagation_setup.acceleration.spherical_harmonic_gravity(12,12),
        propagation_setup.acceleration.aerodynamic()
    ],
    Moon=
    [
        propagation_setup.acceleration.point_mass_gravity()
    ],
    Jupiter=
    [
        propagation_setup.acceleration.point_mass_gravity()
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
    inclination = np.deg2rad(97.5919),
    argument_of_periapsis = np.deg2rad(0.0),
    longitude_of_ascending_node = np.deg2rad(90.0),
    true_anomaly = np.deg2rad(0.0)
)

initial_state_CHESS2 = conversion.keplerian_to_cartesian(
    gravitational_parameter = earth_gravitational_parameter,
    semi_major_axis = 6928136,
    eccentricity = 0.0424,
    inclination = np.deg2rad(97.5919),
    argument_of_periapsis = np.deg2rad(0.0),
    longitude_of_ascending_node = np.deg2rad(90.0),
    true_anomaly = np.deg2rad(0.0)
)

initial_state=np.hstack([initial_state_CHESS1,initial_state_CHESS2])

# Variables to Export
dependent_variables_to_save = [
    propagation_setup.dependent_variable.relative_position("CHESS1","Earth"),
    propagation_setup.dependent_variable.single_acceleration_norm(
        propagation_setup.acceleration.cannonball_radiation_pressure_type, "CHESS1", "Sun"
    ),
    propagation_setup.dependent_variable.relative_position("CHESS2","Earth"),
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

np.savetxt('PropagationResults.dat', result2array(dynamics_simulator.dependent_variable_history))



