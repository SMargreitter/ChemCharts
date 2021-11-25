from typing import List

from rdkit.DataStructs.cDataStructs import ExplicitBitVect
from rdkit.Chem.AllChem import Mol
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import MACCSkeys
from copy import deepcopy

from chemcharts.core.container.smiles import Smiles


class FingerprintContainer:
    """ Class object which contains a list of fingerprints and its name.
        input:
            list of fingerprints and string which refers to the name of the fingerprints
        output:
            __len__method gives back the length of the fingerprint list
            with indexing items can be returned or deleted
            __iter__ and __getitem__ the same???
        """
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
    def __init__(self, name: str, fingerprint_list: List[ExplicitBitVect] = None):
        self.name = name
        self.fingerprint_list = [] if fingerprint_list is None else fingerprint_list

    def __repr__(self) -> str:
        return f"Name: {self.name}, first fp: {self.fingerprint_list[0]}" \
               f"length: {len(self.fingerprint_list)}"

    def __str__(self):
        return self.__repr__()

    def __iter__(self):
        return iter(self.fingerprint_list)

    def __len__(self) -> int:
        return len(self.fingerprint_list)

    def __getitem__(self, item) -> ExplicitBitVect:
        return self.fingerprint_list[item]

    def __setitem__(self, obj, idx: int):
        self.fingerprint_list[idx] = obj

    def __delitem__(self, item):
        del self.fingerprint_list[item]

    def __add__(self, obj):
        copy_self = deepcopy(self)
        obj = deepcopy(obj)
        copy_self.name = "aggregated_fingerprint"
        copy_self.fingerprint_list.append(obj.fingerprint_list)
        return copy_self


class FingerprintGenerator:
    """ Transforms MolSmiles to fingerprints by using the RDKit fingerprints (standard, Morgan and
        MACCS) and then adds them to the fingerprint_list of an object of the FingerprintContainer class.
        input:
           list of MolSmiles -- every smile encodes one molecule, the characters represent chemical
           elements
        output:
           object of the FingerprintContainerClass -- fingerprints are represented as bit vectors (lists
           with 0 and 1 or numbers) and are added to the fingerprint_list
    """
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

    def __init__(self, smiles_obj: Smiles):
        self.mol_list = self.make_mol_list(smiles_obj.smiles_list)

    def __str__(self):
        return self.__repr__()

    def __iter__(self):
        return iter(self.mol_list)

    @staticmethod
    def make_mol_list(column: List[str]) -> List[Mol]:
        """ Transforms smiles to Mol's and adds them to the mol_list
            input:
                list of smiles
            output:
                list of RDkit molecules
        """
        mol_list = []
        for item in column:
            mol_list.append(Chem.MolFromSmiles(item))
        return mol_list

    def generate_fingerprints(self) -> FingerprintContainer:
        """ Transforms internal MolSmiles to fingerprints by using the STANDARD RDKit fingerprint function
            and then adds them to the fingerprint_list of an object of the FingerprintContainer class.
            output:
                an object of the FingerprintContainerClass, containing a list of fingerprints
        """
        fingerprint_buffer = []
        for mol in self.mol_list:
            fingerprint = Chem.RDKFingerprint(mol)
            fingerprint_buffer.append(fingerprint)
        return FingerprintContainer(name="standard_fingerprint", fingerprint_list=fingerprint_buffer)

    def generate_fingerprints_morgan(self, useFeatures=False) -> FingerprintContainer:
        """ Transforms internal MolSmiles to fingerprints by using the MORGAN RDKit fingerprint function
            and then adds them to the fingerprint_list of an object of the FingerprintContainer class.
            output:
                an object of the FingerprintContainer class, containing a list of fingerprints
        """
        fingerprint_buffer = []
        for mol in self.mol_list:
            fingerprint = AllChem.GetMorganFingerprintAsBitVect(mol, radius=3, useFeatures=useFeatures)
            fingerprint_buffer.append(fingerprint)
        return FingerprintContainer(name="morgan_fingerprint", fingerprint_list=fingerprint_buffer)

    def generate_fingerprints_maccs(self) -> FingerprintContainer:
        """ Transforms internal MolSmiles to fingerprints by using the MACC RDKit fingerprint function
            and then adds them to the fingerprint_list of an object of the FingerprintContainer class.
            output:
                an object of the FingerprintContainer class, containing a list of fingerprints
        """
        fingerprint_buffer = []
        for mol in self.mol_list:
            fingerprint = MACCSkeys.GenMACCSKeys(mol)
            fingerprint_buffer.append(fingerprint)
        return FingerprintContainer(name="maccs_fingerprint", fingerprint_list=fingerprint_buffer)
