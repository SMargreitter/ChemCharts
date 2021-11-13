from typing import List


class Smiles:
    def __init__(self, smiles_list: List[str]):
        if not isinstance(smiles_list, list):
            raise TypeError("Needs to be a list.")
        self.smiles_list = smiles_list

    def __getitem__(self, item) -> str:
        return self.smiles_list[item]

    def __len__(self) -> int:
        return len(self.smiles_list)
