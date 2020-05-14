from mapper_class import MAPPER

mapper = MAPPER("dem.asc", "../input")
mapper.add_horizon("bottom_sh.asc")
mapper.add_horizon("horizon_21.asc")

print(mapper.horizon_dims)
print(mapper.horizons)

import matplotlib.pyplot as plt
import numpy as np
for i in range(len(mapper.horizons)):
    _h = np.ma.masked_less(mapper.horizons[i], 0.0)
    _n = mapper.horizon_dims[i]
    plt.imshow(np.reshape(_h, (_n[0], _n[1])))
    plt.show()
