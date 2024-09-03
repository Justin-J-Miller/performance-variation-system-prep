from openmm.app import *
from openmm import *
from openmm.unit import *
from sys import stdout

hmass=2

gro=GromacsGroFile('./start.gro')
top=GromacsTopFile('./topol.top', periodicBoxVectors=gro.getPeriodicBoxVectors(),
        includeDir='./')

system=top.createSystem(nonbondedMethod= PME, nonbondedCutoff= 1 * nanometers, 
                        constraints=HBonds, hydrogenMass=hmass*amu)

integrator = XmlSerializer.deserialize(open('../integrator.xml').read())

simulation = simulation.Simulation(top.topology, system, integrator)
simulation.context.setPositions(gro.positions)

print('Loaded system, minimizing.')
simulation.minimizeEnergy()

State = simulation.context.getState(getPositions=True, getVelocities=True,
                                    getForces=True, getEnergy=True)

print('Serializing State')
# Serialize state
state_filename = f'state.xml'
with open(state_filename, 'w') as f:
    input = XmlSerializer.serialize(State)
    f.write(input)

print('Serializing System')
# Serialize system
with open(f'./system.xml','w') as f:
    input = XmlSerializer.serialize(system)
    f.write(input)
print('wrote systems')