from typing import List

from rdkit.DataStructs.cDataStructs import ExplicitBitVect
from rdkit.Chem.AllChem import Mol
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import MACCSkeys
from copy import deepcopy

from chemcharts.core.container.smiles import Smiles

from chemcharts.core.utils.enums import FingerprintEnum
_FE = FingerprintEnum


class FingerprintContainer:
    """
       Class object which contains a list of fingerprints and its name.

        ...

        Attributes (required)
        ----------
        name : str
            allocated name of the fingerprint
        fingerprint_list : List[ExplicitBitVect]
            list of fingerprints

        Methods
        -------
        __repr__:
            returns a string with the name, list and the length of the fingerprint
        __len__:
            returns the length of the fingerprint_list
        __add__:
            returns an object with an added fingerprint_list
    """

    def __init__(self, name: str = "", fingerprint_list: List[ExplicitBitVect] = None):
        self.name = name
        self.fingerprint_list = [] if fingerprint_list is None else fingerprint_list

    def __repr__(self) -> str:
        return f"Name: {self.name}/ first fp: {self.fingerprint_list[0]}/" \
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
        copy_self.name = _FE.AGGREGATED_FINGERPRINT
        copy_self.fingerprint_list += obj.fingerprint_list
        return copy_self


class FingerprintGenerator:
    """
        Transforms MolSmiles to fingerprints by using the RDKit fingerprints (standard, Morgan and
        MACCS) and then adds them to the fingerprint_list of an object of the FingerprintContainer.

        ...

        Attributes (required)
        ----------
        smiles_obj : Smiles
            object contains a list of MolSmiles (every smile encodes one molecule)
            eg [O=C1c2ccccc2C(=O)N1CCC1=Cc2ccccc2CCC1, ...] -> the characters represent chemical elements

        Methods
        -------
        make_mol_list <column: List[str]>:
            returns a list of MolSmiles
        generate_fingerprints:
            transforms MolSmiles to fingerprints by using the RDKit standard fingerprint, adds them to the
            fingerprint_list of an object of the FingerprintContainer and returns it
        generate_fingerprints_morgan <useFeatures=False>:
            transforms MolSmiles to fingerprints by using the RDKit Morgan fingerprint, adds them to the
            fingerprint_list of an object of the FingerprintContainer and returns it
        generate_fingerprints_maccs:
            transforms MolSmiles to fingerprints by using the RDKit MACCS fingerprint, adds them to the
            fingerprint_list of an object of the FingerprintContainer and returns it
    """

    def __init__(self, smiles_obj: Smiles):
        self.mol_list = self.make_mol_list(smiles_obj.smiles_list)

    def __str__(self):
        return self.__repr__()

    def __iter__(self):
        return iter(self.mol_list)

    @staticmethod
    def make_mol_list(column: List[str]) -> List[Mol]:
        """
            Transforms object of Smiles to Mol's and adds them to the mol_list.

            Parameters
            ----------
            column: List[str]
                list of objects of Smiles

            Returns
            -------
            mol_list
                a list containing MolSmiles
        """

        mol_list = []
        for item in column:
            mol_list.append(Chem.MolFromSmiles(item))
        return mol_list

    def generate_fingerprints(self) -> FingerprintContainer:
        """
            Transforms internal MolSmiles to fingerprints by using the STANDARD RDKit fingerprint function,
            adds them to the fingerprint_list of an object of the FingerprintContainer and returns it.

            Returns
            -------
            FingerprintContainer
                an object of the FingerprintContainer, containing a list of fingerprints
        """

        fingerprint_buffer = []
        for mol in self.mol_list:
            fingerprint = Chem.RDKFingerprint(mol)
            fingerprint_buffer.append(fingerprint)
        return FingerprintContainer(name=_FE.STANDARD_FINGERPRINT, fingerprint_list=fingerprint_buffer)

    def generate_fingerprints_morgan(self, useFeatures=False) -> FingerprintContainer:
        """
            Transforms internal MolSmiles to fingerprints by using the MORGAN RDKit fingerprint function,
            adds them to the fingerprint_list of an object of the FingerprintContainer and returns it.

            Parameters
            ----------
            useFeatures: Bool
                default = False

            Returns
            -------
            FingerprintContainer
                an object of the FingerprintContainer, containing a list of fingerprints
        """

        fingerprint_buffer = []
        for mol in self.mol_list:
            fingerprint = AllChem.GetMorganFingerprintAsBitVect(mol, radius=3, useFeatures=useFeatures)
            fingerprint_buffer.append(fingerprint)
        return FingerprintContainer(name=_FE.MORGAN_FINGERPRINT, fingerprint_list=fingerprint_buffer)

    def generate_fingerprints_maccs(self) -> FingerprintContainer:
        """
            Transforms internal MolSmiles to fingerprints by using the MACCS RDKit fingerprint function,
            adds them to the fingerprint_list of an object of the FingerprintContainer and returns it.

            Returns
            -------
            FingerprintContainer
                an object of the FingerprintContainer, containing a list of fingerprints
        """

        fingerprint_buffer = []
        for mol in self.mol_list:
            fingerprint = MACCSkeys.GenMACCSKeys(mol)
            fingerprint_buffer.append(fingerprint)
        return FingerprintContainer(name=_FE.MACCS_FINGERPRINT, fingerprint_list=fingerprint_buffer)
