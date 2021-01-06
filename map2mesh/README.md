# map2mesh

A python-based workflow to map discrete values to a mesh.
Current application is to prescribe geological layer types to general
unstructured meshes for integrated hydrological modeling.

![figure](../img/fig-layer-0021.png)

## Dependencies

* `numpy` for array handling and interpolation between node values
* `matplotlib` to visualize array data
* `tinerator` for geodata handling and interpolation of values to mesh
* `pyvista` to visualize mesh
