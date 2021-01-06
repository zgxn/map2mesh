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

    def __init__(self, filepath:str, dirpath:str = "input", layerpath:str = "layer-thickness.dat", surfmesh = None):

        self.ok = "[OK]"
        self.na = "[!!]"

        self.dirpath = dirpath
        self.dem = tin.load.from_file(dirpath + "/" + filepath)

        self.layers = np.genfromtxt(dirpath + "/" + layerpath, comments = '#', delimiter = ',')
        
        self.horizons = []

        self.surfmesh = surfmesh
        if surfmesh is not None:
            self.dem._surface_mesh = None

    def do_mesh(self, dx_min:float, fname:str="_mesh.exo", dx_max:float = 0.0, eps:float = 1.0e-2):
        '''
        generate the mesh that we will map the values onto
        '''
        if dx_max < dx_min:
            self.dem.build_uniform_triplane(dx_min)
        else:
            self.dem.watershed_delineation(eps)
            self.dem.build_refined_triplane(dx_min, dx_max)

        tin.dump.to_avs(self.dem, '_surface_mesh')
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

    def generate_ids_per_layer(self):
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
            _up  = np.zeros((ny, nx), dtype=int) - 9999 # store the values above the coordinate
            _do  = np.zeros((ny, nx), dtype=int) - 9999 # store the values below the coordinate
            _surf = _top - 0.5 * layer_dzs[i]           # compute the surface coordinate
#            _soil_ids = np.zeros((ny, nx)) - 100

            for row in range(ny):
                for col in range(nx):
                    _z = _surf[row, col]
                    _ab = 10000.0
                    _be = 10000.0
                    if _z > self.horizons[0][row, col]: #or (self.dem.dem[row, col] - _z) < 1.5:
                        _up[row, col] = 100
#                        print(self.ok + " %f > %f" %(_z, self.horizons[0][row, col]))
                    elif _z > 0.0:
#                        print(self.ok + " %f < %f" %(_z, self.horizons[0][row, col]))
                        for horizon_index in range(len(self.horizons)):
                            _h = self.horizons[horizon_index]
                            _delta = _h[row, col] - _z
                            if _delta >= 0.0 and _delta < _ab:
                                _ab = _delta
                                _up[row, col] = horizon_index + 1
                            elif _delta < 0.0 and np.abs(_delta) < _be:
                                _be = np.abs(_delta)
                                _do[row, col] = horizon_index + 1

            _up[np.where(_up < -1000)] = _do[np.where(_up < -1000)]
            print(self.ok + " geology type mapped to %f m." %np.mean(np.ma.masked_less(_top, 0.0)))
            _top = _surf - 0.5 * layer_dzs[i]
            print(self.ok + " delta z is %f m." %(np.mean(np.ma.masked_less(self.dem.dem, 0.0)) - np.mean(np.ma.masked_less(_top, 0.0))))
            mapped_vals.append(_up)

            np.savetxt("soil-id-layer-" + str(i) + ".asc", _up, delimiter = " ")

        return mapped_vals

    def map2mesh(self, dx_min:float, dx_max:float = 0.0, eps:float = 1.0e-2):

        if self.surfmesh is None:
            self.do_mesh(dx_min, dx_max = dx_max)
        
        vals = self.generate_ids_per_layer()

        for i in range(len(vals)):
            val = vals[len(vals) - 1 - i].astype(int)            
            self.dem.add_attribute(val, layers=[i + 1], dtype=int)

        xll = self.dem.xll_corner
        yll = self.dem.yll_corner

        _faceset_top_bottom = tin.facesets.basic(has_top = True, has_bottom = True, has_sides = False)
        _faceset_sidesets = tin.facesets.sidesets(np.array([[xll + 4485.46, yll + 79.7274], [xll + 4895.0, yll + 455.0], [xll + 5045.0, yll + 1125.0], [xll + 1885.0, yll + 4595.0], [xll + 1325.0, yll + 4395.0]]), top_layer = False)
        _faceset_outlet = tin.facesets.sidesets(np.array([[xll + 5045.0, yll + 1125.0], [xll + 4895.0, yll + 455.0]]), top_layer = True)
        _faceset_north = tin.facesets.sidesets(np.array([[xll + 1325.0, yll + 4395.0], [xll + 1885.0, yll + 4595.0]]), top_layer = True)

        tin.plot.plot_facesets(self.dem, [_faceset_top_bottom, _faceset_sidesets, _faceset_outlet, _faceset_north])

        tin.dump.to_avs(self.dem, "_mesh")
        tin.dump.to_exodus(self.dem, "_mesh.exo", facesets = [_faceset_top_bottom, _faceset_sidesets, _faceset_outlet, _faceset_north])
