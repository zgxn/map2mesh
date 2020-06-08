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
mapper.add_horizon("horizon_22.asc")
mapper.add_horizon("horizon_23b.asc")
mapper.add_horizon("horizon_23c.asc")
mapper.add_horizon("horizon_23d.asc")
mapper.add_horizon("horizon_26.asc")
mapper.add_horizon("horizon_28.asc")

mapper.map2mesh(80.0)

pv.read("_mesh.exo").plot(show_edges=True)

