from typing import List
from copy import deepcopy


class Smiles:
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
    def __init__(self, smiles_list: List[str] = None):
        smiles_list = [] if smiles_list is None else smiles_list
        if not isinstance(smiles_list, list):
            raise TypeError("Needs to be a list.")
        self.smiles_list = smiles_list

    def __len__(self) -> int:
        return len(self.smiles_list)

    def __getitem__(self, idx: int) -> str:
        return self.smiles_list[idx]

    def __setitem__(self, obj, idx: int):
        self.smiles_list[idx] = obj

    def __add__(self, obj):
        copy_self = deepcopy(self)
        obj = deepcopy(obj)
        copy_self.smiles_list += obj.smiles_list
        return copy_self
