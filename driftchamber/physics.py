from numpy.linalg import norm


def relativistic_energy(mass, momentum):
    return (mass**2 + norm(momentum**2))**0.5


def relativistic_momentum(energy, mass):
    return (energy**2 - mass**2)**0.5
