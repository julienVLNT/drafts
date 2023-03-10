import matplotlib.pyplot as plt
import matplotlib.tri    as tri
import mesh              as mesh
import numpy             as np
import scipy.interpolate as sci

class ScalarField():

    def __init__(self, mesh: mesh.Mesh, values: np.ndarray) -> None:
        self.mesh   = mesh
        self.values = values
        return None
    


class TensorField():

    def __init__(self, mesh: mesh.Mesh, values: np.ndarray) -> None:
        self.mesh   = mesh
        self.values = values
        return None


    def compute_invariant_i2(self):
        self.i2 = np.sqrt(    np.power(self.values[0, :3, :], 2).sum(axis=0) \
                         + 2 *np.power(self.values[0, 3:, :], 2).sum(axis=0) )
        
    def compute_invariant_j2(self):
        self.j2 = np.sqrt( 
                           3./2 *np.power(self.values[0, :3, :] -1./3 *self.values[0, :3, :].sum(axis=0) /3.0, 2).sum(axis=0) \
                         + 3. *np.power(self.values[0, 3:, :], 2).sum(axis=0)
                         )