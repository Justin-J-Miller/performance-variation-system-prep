from openmm import *
from openmm.app import *
from openmm.unit import *
import time
from glob import glob
import os.path

n_steps=10000

runs = glob('*/system.xml')
for run in runs: 
	basedir = os.path.dirname(run)
	print(basedir)

	print('Loading System')
	system = XmlSerializer.deserialize(open(f'{basedir}/system.xml').read())
	print('Loading State')
	state = XmlSerializer.deserialize(open(f'{basedir}/state.xml').read())
	print('Loading Integrator')
	integrator = XmlSerializer.deserialize(open('integrator.xml').read())
	print('Setting Context')
	context = Context(system, integrator)
	context.setState(state)
	print('Running simulation, system has:')
	print(f'{system.getNumParticles()} particles')
	print(f'{system.getNumForces()} forces.')
	print(f'Box Vectors: {system.getDefaultPeriodicBoxVectors()}.')
	integrator.step(10)
	t1 = time.time()
	integrator.step(n_steps)
	t2 = time.time()
	elapsedDays = (t2-t1)/86400.0
	elapsedNs = (n_steps*integrator.getStepSize()).value_in_unit(nanosecond)
	print(f'Perforance: {elapsedNs/elapsedDays} ns/day')

	print('\n \n \n')