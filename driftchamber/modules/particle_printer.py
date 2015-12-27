from driftchamber.core.module import Module

class ParticlePrinter(Module):

    def event(self, datastore):
        particle = datastore.get('particle')
        
        print('Particle: ', particle.name)
        print('Particle position: ', particle.position)
        print('Particle momentum: ', particle.momentum)
