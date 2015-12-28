from numpy.linalg import norm


def relativistic_energy(mass, momentum):
    return (mass**2 + norm(momentum**2))**0.5
