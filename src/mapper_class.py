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

    def __init__(self, filepath:str, dirpath:str = "input"):

        self.ok = "[OK]"
        self.na = "[!!]"

        self.dirpath = dirpath
        self.dem = tin.load.from_file(dirpath + "/" + filepath)
        
        self.horizons = []
        self.horizon_dims = []

        # --- A: DBG ---
        # we need to set the lower left corner to 0
        # this must be fixed once the issue in tinerator is solved
        self.dem.xll_corner = 0.0
        self.dem.yll_corner = 0.0
        # --- E: DBG ---

    def add_horizon(self, filepath:str, sep:str = " ", comment_char:str = "#"):

        _horizon = np.genfromtxt(self.dirpath + "/" + filepath,
                                 delimiter = sep, comments = comment_char)
        _ny, _nx = _horizon.shape
        self.horizon_dims.append([_ny, _nx])
        self.horizons.append(_horizon.flatten())

        print(self.ok + " added " + filepath + " to the horizons.")

        



