# tinerator watch

Use case investigations for the mesh generator
[tinerator](https://github.com/lanl/LaGriT/tree/tinerator).

## Known issues

As of Tue Jan 5 16:35:07 PST 2021, the latest version of tinerator
won't carry out multiresolution triangulations and fail with a
`pexpect` exception.

This is related to counterclockwise meshing.  The current work around
is to carry out the triangulation with `counterclockwise = True`.

## Use case

A python-based workflow to map discrete values to a mesh.  Current
application is to prescribe geological layer types to general
unstructured meshes for integrated hydrological modeling.

![figure](img/fig-layer-0021.png)

### Dependencies

* `numpy` for array handling and interpolation between node values
* `matplotlib` to visualize array data
* `tinerator` for geodata handling and interpolation of values to mesh
* `pyvista` to visualize mesh

### License

[BSD-3](./LICENSE)

## Acknowledgment

This work is funded as part of the Watershed Function - Scientific
Focus Area by the U.S. Department of Energy, Office of Science, Office
of Biological and Environmental Research, Award no. DE-AC02-05CH11231.
