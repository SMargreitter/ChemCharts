import numpy as np
from copy import deepcopy


class Embedding:
    """The Embedding class contains dimensionally reduced fingerprints in np-array format."""
    """
      This class currently takes a dimension and a degree of polynomial
      and builds the Smolyak Sparse grid.  We base this on the work by
      Judd, Maliar, Maliar, and Valero (2013).

      Parameters
      ----------
      d : scalar(int)
          The number of dimensions in the grid

      mu : scalar(int) or array_like(int, ndim=1, length=d)
          The &quot;density&quot; parameter for the grid

      Attributes
      ----------
      d, mu : see Parameters

      lb : array_like(float, ndim=2)
          This is an array of the lower bounds for each dimension

      ub : array_like(float, ndim=2)
          This is an array of the upper bounds for each dimension

      cube_grid : array_like(float, ndim=2)
          The Smolyak sparse grid on the domain :math:`[-1, 1]^d`

      grid: : array_like(float, ndim=2)
          The sparse grid, transformed to the user-specified bounds for
          the domain

      inds : list(list(int))
          This is a lists of lists that contains all of the indices

      B : array_like(float, ndim=2)
          This is the B matrix that is used to do lagrange interpolation

      B_L : array_like(float, ndim=2)
          Lower triangle matrix of the decomposition of B

      B_U : array_like(float, ndim=2)
          Upper triangle matrix of the decomposition of B

      Examples
      --------
      >>> s = SmolyakGrid(3, 2)
      >>> s
      Smolyak Grid:
          d: 3
          mu: 2
          npoints: 25
          B: 0.65% non-zero
      >>> ag = SmolyakGrid(3, [1, 2, 3])
      >>> ag
      Anisotropic Smolyak Grid:
          d: 3
          mu: 1 x 2 x 3
          npoints: 51
          B: 0.68% non-zero
        """
    def __init__(self, np_array: np.ndarray = None):
        self.np_array = np.empty((0, 2), float) if np_array is None else np_array

    def __repr__(self) -> str:
        return f"Embedding: {self.np_array}"

    def __str__(self):
        return self.__repr__()

    def __len__(self):
        return self.np_array.size

    def __getitem__(self, item):
        if isinstance(item, (int, slice)):
            return self.np_array[item]
        return [self.np_array[i] for i in item]

    def __setitem__(self, obj, idx: int):
        self.np_array[idx] = obj

    def __add__(self, obj):
        copy_self = deepcopy(self)
        obj = deepcopy(obj)
        copy_self.np_array = np.concatenate((copy_self.np_array, obj.np_array))
        return copy_self
