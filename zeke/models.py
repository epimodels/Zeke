
##################################################
# Python implementation of Zombie Epidemic Models#
# By: Eric Lofgren                               #
# Network Dynamics and Simulation Science Lab    #
# Virginia Bioinformatics Institute              #
# Email: lofgrene@vbi.vt.edu                     #
##################################################

# Based on ../demos/ZombieModels.py
from scipy import integrate
import numpy
from time import sleep


def ZombieSIR(infect_prob, infect_duration):
    """
    ### Susceptible-Zombie-Dead mathematical model.
    ### Takes two arguments:
    ### Beta: A probability of infection
    ### Gamma: Infection duration in days
    """
    #Parameter Values and Initial Conditions
    S0 = 0.9999
    I0 = 0.0001
    R0 = 0.
    InitialPop = (S0, I0, R0)
    beta = infect_prob
    gamma = infect_duration
    t_end = 125.
    t_start = 1.
    t_step = 0.1
    numpy.arange(t_start, t_end, t_step)

    # Calculate R_0
    R_0 = beta/gamma

    #Solving the differential equation. Solves over t for initial conditions
    # PopIn
    def SIR_System(t, InitialPop):
    #Creating an array of equations
        SIR_Equations = numpy.zeros((3))
        SIR_Equations[0] = -beta * (InitialPop[0] * InitialPop[1])
        SIR_Equations[1] = (
            beta * (InitialPop[0] * InitialPop[1]) - gamma * InitialPop[1])
        SIR_Equations[2] = gamma * InitialPop[1]
        return SIR_Equations

    scipy_integrate_ode = integrate.ode(SIR_System)

    # BDF method suited to stiff systems of ODEs
    scipy_integrate_ode.set_integrator('vode', nsteps=500, method='bdf')
    scipy_integrate_ode.set_initial_value(InitialPop, t_start)

    time_series = []
    outcome_series = []

    count = 0
    while scipy_integrate_ode.successful() and scipy_integrate_ode.t < t_end:
        count += 1
        scipy_integrate_ode.integrate(scipy_integrate_ode.t + t_step)
        time_series.append(scipy_integrate_ode.t)
        outcome_series.append(scipy_integrate_ode.y)

    if count == 1:  # Something is wrong
        return False

    t = numpy.vstack(time_series)
    s, i, r = numpy.column_stack(outcome_series)

    return t, s, i, r, R_0


def ZombieSEIR(infect_prob, infect_duration, latent_period):
    """
    ### Zombie epidemic model with latent infection period.
    ### Takes three arguments:
    ### Beta: A probability of infection
    ### Gamma: Infection duration in days
    ### Alpha: A latent (non-zombie infected) period in days
    """
    #Parameter Values and Initial Conditions
    S0 = 0.9999
    E0 = 0.
    I0 = 0.0001
    R0 = 0.
    InitialPop = (S0, E0, I0, R0)
    beta = infect_prob
    gamma = infect_duration
    alpha = latent_period
    t_end = 125.
    t_start = 1.
    t_step = 0.1
    numpy.arange(t_start, t_end, t_step)

    #Solving the differential equation. Solves over t for initial conditions
    # PopIn
    def SEIR_System(t, InitialPop):
    #Creating an array of equations
        SEIR_Equations = numpy.zeros((4))
        SEIR_Equations[0] = -beta * (InitialPop[0] * InitialPop[2])
        SEIR_Equations[1] = (
            beta * (InitialPop[0] * InitialPop[2]) - alpha * InitialPop[1])
        SEIR_Equations[2] = alpha * InitialPop[1] - gamma * InitialPop[2]
        SEIR_Equations[3] = gamma * InitialPop[2]
        return SEIR_Equations

    scipy_integrate_ode = integrate.ode(SEIR_System)

    # BDF method suited to stiff systems of ODEs
    scipy_integrate_ode.set_integrator('vode', nsteps=500, method='bdf')
    scipy_integrate_ode.set_initial_value(InitialPop, t_start)

    time_series = []
    outcome_series = []

    count = 0
    while scipy_integrate_ode.successful() and scipy_integrate_ode.t < t_end:
        count += 1
        scipy_integrate_ode.integrate(scipy_integrate_ode.t + t_step)
        time_series.append(scipy_integrate_ode.t)
        outcome_series.append(scipy_integrate_ode.y)

    if count == 1:  # Something is wrong
        return False

    t = numpy.vstack(time_series)
    s, e, i, r = numpy.column_stack(outcome_series)

    return t, s, e, i, r


def Haven(infect_prob_free, infect_prob_safe, infect_duration,
          latent_period, kill_prob, time_to_shelter):

    """
    ### "Safe Haven" Model - Survivors make for shelter, can fight back
    ### Takes six arguments:
    ### Psi: Rate at which survivors find shelter
    ### Beta_F: A probability of infection for unsheltered survivors
    ### Beta_H: A probability of infection for sheltered survivors
    ### Gamma: Infection duration in days
    ### Alpha: A latent (non-zombie infected) period in days
    ### Kappa: Probability a sheltered survivor x zombie encounter ends with a
    ###  dead zombie
    """
    #Parameter Values and Initial Conditions
    S0 = 0.9999
    E0 = 0.
    I0 = 0.0001
    R0 = 0.
    H0 = 0.
    C0 = 0.
    InitialPop = (S0, H0, E0, I0, C0, R0)
    psi = time_to_shelter
    beta_f = infect_prob_free
    beta_h = infect_prob_safe
    gamma = infect_duration
    alpha = latent_period
    kappa = kill_prob
    t_end = 125.
    t_start = 1.
    t_step = 0.1
    numpy.arange(t_start, t_end, t_step)

    #Solving the differential equation. Solves over t for initial conditions
    # PopIn
    def Haven_System(t, InitialPop):
    #Creating an array of equations
        Haven_Equations = numpy.zeros((6))
        Haven_Equations[0] = -beta_f * (
            InitialPop[0] * InitialPop[3]) - psi * InitialPop[0]
        Haven_Equations[1] = (
            psi * InitialPop[0] - beta_h * InitialPop[1] * InitialPop[3])
        Haven_Equations[2] = (
            beta_f * (InitialPop[0] * InitialPop[3]) + beta_h * InitialPop[1] *
            InitialPop[3] - alpha * InitialPop[2])
        Haven_Equations[3] = (
            alpha * InitialPop[2] - gamma * InitialPop[3] - kappa *
            InitialPop[3] * InitialPop[1])
        Haven_Equations[4] = kappa * InitialPop[3] * InitialPop[1]
        Haven_Equations[5] = gamma * InitialPop[3]
        return Haven_Equations

    scipy_integrate_ode = integrate.ode(Haven_System)

    # BDF method suited to stiff systems of ODEs
    scipy_integrate_ode.set_integrator('vode', nsteps=500, method='bdf')
    scipy_integrate_ode.set_initial_value(InitialPop, t_start)

    time_series = []
    outcome_series = []

    count = 0
    while scipy_integrate_ode.successful() and scipy_integrate_ode.t < t_end:
        count += 1
        scipy_integrate_ode.integrate(scipy_integrate_ode.t + t_step)
        time_series.append(scipy_integrate_ode.t)
        outcome_series.append(scipy_integrate_ode.y)

    if count == 1:  # Something is wrong
        return False

    t = numpy.vstack(time_series)
    s, h, e, i, c, r = numpy.column_stack(outcome_series)

    return t, s, h, e, i, c, r