from mapper_class import MAPPER
import matplotlib.pyplot as plt
import numpy as np
import pyvista as pv

mapper = MAPPER("dem.asc", "../input")

# --- A: DBG ---
# we need to set the lower left corner to 0
# this must be fixed once the issue in tinerator is solved
mapper.dem.xll_corner = 0.0
mapper.dem.yll_corner = 0.0
# --- E: DBG ---

mapper.add_horizon("bottom_sh.asc")
mapper.add_horizon("horizon_21.asc")

#for i in range(len(mapper.horizons)):
#    _h = np.ma.masked_less(mapper.horizons[i], 0.0)
#    plt.imshow(_h)
#    plt.show()

names = [ - 0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5 ]
vals = mapper.map_horizons_to_layers()

mapper.do_mesh(80.0)

counter = 1
for v in vals:
    print("[OK] %d" %counter)
    plt.imshow(np.ma.masked_less(v, -9000), interpolation = 'none', cmap = 'Spectral_r')
    plt.clim(0, 7)
    cb = plt.colorbar(ticks = range(8), boundaries = names)
    plt.show()
    counter = counter + 1

pv.read("_mesh.exo").plot()
