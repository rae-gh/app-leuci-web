
# To do list
(notes additional to github issues)

## Goal for 17/3/24
- mat mult fixed
- Fo and Fc needed for replication of plots
- spline method add
- relicated on google colab the paper I have written

## Bugs
- choosing linear from settings doesn;t work on prod server, it doesn;t change anythong
- Uploading doesn;t appear on Slice screen - it is blank
- Don;t start uploading again if it is already uploading - check existence of file, if it is there, don't start again (can be deleted from admin)
- When I change interp method it uses old one to calc but new one to decide which derivs to do
- If I navigate off the end of the list for the atoms I get an error
- have I got determinant and inverse wrong comparing with numpy

## TO DO
- Numpy migration - delete old code, serious testing, and also change all the angles in v3
- visual elements need to be in state so eg hue, bar, plot, three type don;t change
- Add navigation to the spacetransform class
- add a reverse hue option
- hook navigation up to examples and to leuci-web
- Clear Memory in admin needs to be implemented
- Long GET link needed on Scratch
- Document leuci-map with readthedocs
- Projection
- Raw matrix slice - cross sections
- in leuci-map add "get nearest maxima" or minima
- in leuci-map add adjust pdb file to maxima !!!!!
- create triv-div library: I had an idea that resampling could be used on a density map itself. Mark suggests comparing pseudo density and a real structure and thus resurrecting Alcraft-Williams divergence! No idea if this will work but it feels like a relevant idea. In fact, it is perfect for AW-Trivial Divergence. ALso can be used to compare structures.
- Add in the compare function that I started, Mark thinks it is important for first version
- docstring everythong with this style:
----------------------------------------------------
  """Generates the RGB image and depth map from model prediction.
    Args:
        model: The MLP model that is trained to predict the rgb and
            volume density of the volumetric scene.
        rays_flat: The flattened rays that serve as the input to
            the NeRF model.
        t_vals: The sample points for the rays.
        rand: Choice to randomise the sampling strategy.
        train: Whether the model is in the training or testing phase.
    Returns:
        Tuple of rgb image and depth map.
    """
----------------------------------------------------

## Missing functionaility
- Add EM maps!!!!
- add bspline method
- implement diff density Fo Fc options
  - could it set off download of diff in another thread to seppd things up
  - mfunc needs to hold both diff objs and take FoFc

## DONE
- speed up the intrpolation uing numpy in m3 classes: make it opitonal, this needs serious testin
 - use jax and numba and @JIT decorator
 https://jax.readthedocs.io/en/latest/notebooks/autodiff_cookbook.html
 https://numba.pydata.org/numba-doc/latest/user/jit.html
- make my c# version match numpy
- speed up usin numpy in just the interpolation library
-  make it density OR linear OR laplacian to save time, or ALL 3 for existing screen
- user identidication in admin
- Javascript for slices fully implemented, ready for first version
- Make a slice in leuci-map - with just nearest neighbour to start with
- - To do this restructure the libs to have a map (electron density) / xyz (space tranform) / pol (iterp) / 
- Hook in leucilib slice to Slice
- Add some collab pages demonstrating some of the links and some of the simple functionality
- Get a slice on google collab with just leuci-lib to demo the aggregation of libraries
- FIX: 1ejg doesn;t work for key->coords in map, index error

## Major enhancements
- superpoisiton 
- image registration

## Notes
- Start without the navigation getting everything visible typeing in the coords
- For writeup, show also the libraries and the documentation for those
- Interpretation and tools needed
 - bfactors, occupancy, motion...


