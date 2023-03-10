import adelio         as io
import matplotlib.tri as tri
import numpy          as np
import scipy          as sp



def field2pic(source: io.Pfile, name: str, timestep: int) -> tuple:

    # Read the connectivity table of the faces
    facet = source.read_faces()
    
    # Extract the ids of the first facet's vertices
    id  = np.where(facet[:, 0]==1)[0]
    id  = np.unique(facet[id, 1:4].flatten())
    
    # Read coordinates ('x', 'z')
    coords = source.read_coords([timestep], ['x', 'z'])

    # Extract the first facet's coordinates
    coords = coords[0, :, id-1].transpose()

    # Build the triangulation
    mesh = tri.Triangulation(coords[0, :], coords[1, :])

    # Read the data related to ['s', 'e', 'd'] (name)
    if name == "s":
        field = source.read_fields([timestep], source.fields[:6])
    
    elif name == "e":
        field = source.read_fields([timestep], source.fields[6:12])

    elif name == "d":
        field = source.read_fields([timestep], source.fields[12:18])

    else:
        raise NotImplementedError
    
    # Compute scalar invariants of the tensor field
    i2 = np.sqrt(    np.power(field[0, :3, :], 2).sum(axis=0) \
                + 2 *np.power(field[0, 3:, :], 2).sum(axis=0) )
    
    p  = field[0, :3, :].sum(axis=0) /3.0
    j2 = np.sqrt( 3./2 *np.power(field[0, :3, :] -1./3*p, 2).sum(axis=0) \
                + 3.   *np.power(field[0, 3:, :], 2).sum(axis=0)         )

    # Compute the nodal representation of i2, j2
    #   - read the connectivity table of the vertices
    conn = source.read_elements()
    #   - build the "reverse topology" representation
    vals = []
    for _ in range(len(id)):
        vals.append([])
    reverse = dict(
        zip(
            id,
            vals
        )
    )
    for i, el in enumerate(conn[:, 1:]):
        for p in el:
            if p in id:
                reverse[p].append(i)
    #   - compute the nodal values as the mean of the values on each element related to this node
    i2 = np.asarray([i2[reverse[i]].sum()/len(reverse[i]) for i in id], dtype=np.float64)
    j2 = np.asarray([j2[reverse[i]].sum()/len(reverse[i]) for i in id], dtype=np.float64)

    # Build discretisation for the two intervals
    xlin = np.linspace(coords[0,:].min(), coords[0,:].max(), 1024, endpoint=True)
    zlin = np.linspace(coords[1,:].min(), coords[1,:].max(), 1024, endpoint=True)
    # Assemble the grid
    xgrid, zgrid = np.meshgrid(xlin, zlin)

    # Interpolate i2, j2 on the regular grid
    i2 = sp.interpolate.griddata( np.swapaxes(coords[:,:], axis1=1, axis2=0), i2[:], (xgrid, zgrid), method='cubic' )
    j2 = sp.interpolate.griddata( np.swapaxes(coords[:,:], axis1=1, axis2=0), j2[:], (xgrid, zgrid), method='cubic' )

    # Fill the NaNs with mean value
    i2 = np.nan_to_num(i2, np.nanmean(i2))
    j2 = np.nan_to_num(i2, np.nanmean(j2))

    # This interpolation is actually the picture.
    return (i2, j2)



def peierls2pic(source: io.Pfile, timestep: int) -> np.ndarray:
    
    # Read the connectivity table of the faces
    facet = source.read_faces()
    
    # Extract the ids of the first facet's vertices
    id  = np.where(facet[:, 0]==1)[0]
    id  = np.unique(facet[id, 1:4].flatten())
    
    # Read coordinates ('x', 'z')
    coords = source.read_coords([timestep], ['x', 'z'])

    # Extract the first facet's coordinates
    coords = coords[0, :, id-1].transpose()

    # Build the triangulation
    mesh = tri.Triangulation(coords[0, :], coords[1, :])

    # Read the data
    field = source.read_fields([timestep], ['Peierls'])[0,...].transpose()

    # Build the nodal representation of the field with the reversed topology
    conn = source.read_elements()
    vals = []
    for _ in range(len(id)):
        vals.append([])
    reverse = dict(
        zip(
            id,
            vals
        )
    )
    for i, el in enumerate(conn[:, 1:]):
        for p in el:
            if p in id:
                reverse[p].append(i)

    field = np.asarray([field[reverse[i]].sum()/len(reverse[i]) for i in id], dtype=np.float64)

    # Build discretisation for the two intervals
    xlin = np.linspace(coords[0,:].min(), coords[0,:].max(), 1024, endpoint=True)
    zlin = np.linspace(coords[1,:].min(), coords[1,:].max(), 1024, endpoint=True)
    # Assemble the grid
    xgrid, zgrid = np.meshgrid(xlin, zlin)

    # Interpolate i2, j2 on the regular grid
    field = sp.interpolate.griddata( np.swapaxes(coords[:,:], axis1=1, axis2=0), field[:], (xgrid, zgrid), method='cubic' )

    # Fill the NaNs with mean value
    peierls = np.nan_to_num(field, np.nanmean(field))

    return peierls



def exp2pic(path: str) -> np.ndarray:

    # Open the file
    field = np.genfromtxt( path, delimiter=',', dtype=np.float64 )
    field = np.nan_to_num(field, np.nanmean(field))
    
    # Padding up to a square
    mean = np.nanmean(field)
    l = min(field.shape)
    L = max(field.shape)
    var = np.ones((L,L), dtype=np.float64) *mean
    var[:, (L-l)//2:(L+l)//2] = field

    return var
