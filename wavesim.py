import meep as mp
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import Video

cell = mp.Vector3(26,30,0)
geometry = [mp.Cylinder(radius=5,axis= mp.Vector3(z=1),
                     center=mp.Vector3(1.7,-3.5),
                     material=mp.Medium(epsilon=12)),
            mp.Cylinder(radius=4,axis=mp.Vector3(z=1),
                        center=mp.Vector3(1.7,-3.5),
                        material = mp.Medium(epsilon=1)),
            mp.Cylinder(radius=5,axis= mp.Vector3(z=1),
                     center=mp.Vector3(1.7,7),
                     material=mp.Medium(epsilon=12)),
            mp.Cylinder(radius=4,axis=mp.Vector3(z=1),
                        center=mp.Vector3(1.7,7),
                        material = mp.Medium(epsilon=1)),
            mp.Block(mp.Vector3(1,30,mp.inf),
                     center=mp.Vector3(7.5,0),
                     material=mp.Medium(epsilon=12))]
            #the axis of the cylinder is the same by default
            
            
pml_layers = [mp.PML(1.0)]
resolution = 30

sources = [mp.Source(mp.ContinuousSource(wavelength=2*(11**0.5), width=20, end_time= 25 ),
                     component=mp.Ez,
                     center=mp.Vector3(7.5,14,0),
                     size=mp.Vector3(1,0))]

 #To have a continuous wave, we can erase the end time. If we keep it, it will create some kind
 #of pulse wave.

sim = mp.Simulation(cell_size=cell,
                    boundary_layers=pml_layers,
                    geometry=geometry,
                    sources=sources,
                    resolution=resolution)


sim.run(until=25)

eps_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Dielectric)
plt.figure()
plt.imshow(eps_data.transpose(), interpolation='spline36', cmap='binary')
plt.axis('off')
plt.show()

ez_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Ez)
plt.figure()
plt.imshow(eps_data.transpose(), interpolation='spline36', cmap='binary')
plt.imshow(ez_data.transpose(), interpolation='spline36', cmap='RdBu', alpha=0.9)
plt.axis('off')
plt.show()



# Prepare the animator and record the steady state response
f = plt.figure(dpi=150)
Animate = mp.Animate2D(sim, fields=mp.Ez, f=f, realtime=False, normalize=False)
sim.run(mp.at_every(0.5,Animate),until=150)


# Process the animation and view it
filename = "wavesim_gauss.gif"
Animate.to_gif(10,filename)

#It will create a gif file in at the same place where your python simulation is.