from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import MACCSkeys

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
    def __init__(self, name: str, fingerprint_list: list):
        self.name = name
        self.fingerprint_list = fingerprint_list

    def __repr__(self) -> str:
        return f"Name: {self.name}, first fp: {self.fingerprint_list[0]}" \
               f"length: {len(self.fingerprint_list)}"

    def __str__(self):
        return self.__repr__()

    def __iter__(self):
        return iter(self.fingerprint_list)

    def __len__(self) -> int:
        return len(self.fingerprint_list)

    def __getitem__(self, item):
        return self.fingerprint_list[item]

    def __delitem__(self, item):
        del self.fingerprint_list[item]


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

    def __init__(self, smiles_obj: Smiles):
        self.mol_list = self.make_mol_list(smiles_obj.smiles_list)

    def __str__(self):
        return self.__repr__()

    def __iter__(self):
        return iter(self.mol_list)

    @staticmethod
    def make_mol_list(column: list) -> list:
        """ Transforms smiles to Mol's and adds them to the mol_list
            input:
                list of smiles
            output:
                list of MolSmiles
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
