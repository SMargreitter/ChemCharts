from typing import List
from copy import deepcopy


class Smiles:
    """The Smiles contains a list of smiles (e.g. [O=C1c2ccccc2C(=O)N1CCC1=Cc2ccccc2CCC1, ...],
       default is None."""

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
