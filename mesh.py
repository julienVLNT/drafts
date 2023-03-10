import matplotlib.pyplot as plt
import matplotlib.tri    as tri
import numpy             as np

# class Mesh3D():

#     def __init__(self, connec: np.ndarray, facets: np.ndarray, coords: np.ndarray) -> None:
#         self.connec = connec
#         self.facets = facets
#         self.coords = coords
#         return None


# class Facet():

#     def __init__(self, m3D: Mesh3D, connec: np.ndarray, coords: np.ndarray) -> None:
#         self.mesh3D = m3D
#         self.connec = connec    # connectivity table, one triangle per line
#         self.coords = coords    # coordinates, one point per line
#         return None


#     def reverse(self) -> None:
#         vals = []
#         for _ in range(len(ids)):
#             vals.append([])

#         reverse = dict(
#             zip(
#                 ids,
#                 vals
#             )
#         )

#         for i, el in enumerate(conn[:, 1:]):
#             for p in el:
#                 if p in ids:
#                     reverse[p].append(i)


class Topology():

    def __init__(self, elements: np.ndarray, facets: np.ndarray, coords: np.ndarray) -> None:
        self.elements = elements
        self.facets   = facets
        self.coords   = coords
        return None
    

    def get_facet(self, N: int) -> None:
        self.facet1 
    


class Topology2d():

    def __init__(self, elements: np.ndarray, coords: np.ndarray) -> None:
        self.elements = elements
        self.coords   = coords
        return None

    def mesh2square(self, Nx: int, Ny: int) -> None:
