# ------------------------------------------------------------------------------
# -- mapper_class.py
#
# -- provides the basic functionalities required to map
# -- discrete values to a mesh
# ------------------------------------------------------------------------------

import tinerator as tin
import numpy as np

class MAPPER():
    '''
    This is the main class of the workflow, and stores all DEM and GIS data
    related to a particular project.
    
    # Attributes
    filepath (str) : Filepath to DEM raster
    dirpath (str)  : Directory path for input files
    '''

    def __init__(self, filepath:str, dirpath:str = "input", layerpath:str = "layer-thickness.dat"):

        self.ok = "[OK]"
        self.na = "[!!]"

        self.dirpath = dirpath
        self.dem = tin.load.from_file(dirpath + "/" + filepath)

        self.layers = np.genfromtxt(dirpath + "/" + layerpath, comments = '#', delimiter = ',')
        
        self.horizons = []

    def do_mesh(self, dx_min:float, fname:str="_mesh.exo", dx_max:float = 0.0, eps:float = 1.0e-2):
        '''
        generate the mesh that we will map the values onto
        '''
        if dx_max < dx_min:
            self.dem.build_uniform_triplane(dx_min)
        else:
            self.dem.watershed_delineation(eps)
            self.dem.build_refined_triplane(dx_min, dx_max)
        self.dem.build_layered_mesh(self.layers[:,1], matids = self.layers[:,0].astype(int))
        tin.dump.to_exodus(self.dem, '_mesh.exo')

            
    def add_horizon(self, filepath:str, sep:str = " ", comment_char:str = "#"):
        '''
        read in the upper boundary of a geological layer and add it
        to a list that will be traversed during the mapping process

        # Attributes
        filepath     : file containing the horizon
        sep          : delimiter in the file
        comment_char : comment indicator in the file
        '''
        _horizon = np.genfromtxt(self.dirpath + "/" + filepath,
                                 delimiter = sep, comments = comment_char)
        self.horizons.append(_horizon)

        print(self.ok + " added " + filepath + " to the horizons.")

        return self.horizons

    def map_horizons_to_layers(self):
        '''
        traverse the list of horizons and create an array that holds
        the geological layer id for each point in the dem
        '''

        mapped_vals = []
        
        n_horizons = len(self.horizons)

        if n_horizons == 0:
            print(self.na + " no layers defined. cannot proceed.")
            import sys
            sys.exit(-1)

        layer_ids = self.layers[:,0]
        layer_dzs = self.layers[:,1]

        n_layers = len(layer_ids)

        ny, nx = self.dem.dem.shape

        _top = np.copy(self.dem.dem)
        
        for i in range(n_layers):
            _up  = np.zeros((ny, nx), dtype=int) - 9999
            _do  = np.zeros((ny, nx), dtype=int) - 9999
            _surf = _top - 0.5 * layer_dzs[i]
            _soil_ids = np.zeros((ny, nx))

            for row in range(ny):
                for col in range(nx):
                    _z = _surf[row, col]
                    _ab = 10000.0
                    _be = 10000.0
                    if _z > self.horizons[0][row, col]:
                        _up[row, col] = 0
                    elif _z > 0.0:
                        for horizon_index in range(len(self.horizons)):
                            _h = self.horizons[horizon_index]
                            _delta = _h[row, col] - _z
                            if _delta >= 0.0 and _delta < _ab:
                                _ab = _delta
                                _up[row, col] = horizon_index
                            elif _delta < 0.0 and np.abs(_delta) < _be:
                                _be = np.abs(_delta)
                                _do[row, col] = horizon_index

            _up[np.where(_up < -1000)] = _do[np.where(_up < -1000)]
            print(self.ok + " geology type mapped to %f m." %np.mean(np.ma.masked_less(_top, 0.0)))
            _top = _surf - 0.5 * layer_dzs[i]
            mapped_vals.append(_up)

            np.savetxt("soil-id-layer-" + str(i) + ".asc", _up, delimiter = " ")

        return mapped_vals
