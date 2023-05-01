
# To do list
(notes additional to github issues)

## Goal for 20/4/24
- fix the problem with the projection on only the atoms area, started making a funciton where the projection takes a range, it works simply in leuci-pol
- speed it up
- make it work peridically


 
## Bugs
- when I untoggle atoms in projection I lose the crystal for the second row

## For 20/4/23
- I have messed about with storage and created a new thread sytem in MapsManager which needs integrating in Slice
- Then I can replicate the speed of a slice view in leuci-map and debug


## TO DO

 - use jax and numba and @JIT decorator
    https://jax.readthedocs.io/en/latest/notebooks/autodiff_cookbook.html
    https://numba.pydata.org/numba-doc/latest/user/jit.html
- add a reverse hue option
- Clear Memory in admin needs to be implemented
- Document leuci-map with readthedocs

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
    Returns:
        Tuple of rgb image and depth map.
    """
----------------------------------------------------

## Missing functionaility
- opt bspline method for large em
- nearest neighbours
- motif matcher
- overlay (cross or in structure)
- compare 2 densities (rad/lap)
- have a python script automatically downloadable for inspection
- eigenvalues
- convert to standard deviations
- pass the actual matrices back and forth and only recalc if ncessary



## DONE
- I have got the angles the wrong way round!!!
- Projection
- Raw matrix slice - cross sections
- make density slider on projection and cross seciotn
- Numpy migration - delete old code, serious testing, and also change all the angles in v3
- visual elements need to be in state so eg hue, bar, plot, three type don;t change
- Add navigation to the spacetransform class
- Don't start uploading again if it is already uploading - check existence of file, if it is there, don't start again (can be deleted from admin)
- If I navigate off the end of the list for the atoms I get an error

## Goal for 17/3/24 - done
- MOST URGENT is sort out the upload and download chain of command. If downloading DO NOT redownload. If uploading DONOT re upload. Make a class checker for these 2 things - downloaded, uploaded, is_downloading, is_uploading and use that in the message status and DO NOT do them again.
- add a wrapping funciton to leuci-maps to reduce the code to make the plots
- make colab page for all the examples, here: https://colab.research.google.com/drive/12_lLJV7MgaRNoQbELvkQ2BEqWirGPi74#scrollTo=_ouMRxVlnO0z
- add in the python download button on slice
- make the python invariant creatable from leuci-pol (take from psu multivarse)
- add 5th degree option
- added projections
- added cross sections
- hook in bspline to web
- hook in fo and fc to web
- add a GET link to web, make the code go differently so it is non async if a GET request
- Long GET link needed on Scratch
- hook navigation up to examples and to leuci-web
- Add EM maps!!!!
- have I got determinant and inverse wrong comparing with numpy
- When I change interp method it uses old one to calc but new one to decide which derivs to do
- the new bspline method shows something really weird on the NOS switch example - looks like out by 1 on a budge up maybe.
55,112,73 in 3u7z is the danger area
- choosing linear from settings doesn;t work on prod server, it doesn;t change anythong
- Uploading doesn;t appear on Slice screen - it is blank
- fix the bspline 3u7z problem (are they the ccp4 same in both versions? It is a boundary error)
- mat mult fixed
- Fo and Fc needed for replication of plots
- spline method add


-----------------------------------------------
- speed up the intrpolation uing numpy in m3 classes: make it opitonal, this needs serious testin
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


