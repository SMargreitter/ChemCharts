import numpy as np

from chemcharts.core.container.embedding import Embedding
from chemcharts.core.container.fingerprint import FingerprintContainer
from chemcharts.core.container.smiles import Smiles


class ChemData:
    """
        A class to represent information about molecules for generating plots.

        ...

        Attributes (required)
        ----------
        smiles_obj : SmilesClass
            object contains a list of smiles (eg [O=C1c2ccccc2C(=O)N1CCC1=Cc2ccccc2CCC1, ...])

        Attributes (optional)
        ----------
        name : str
            should reflect the input data
        epoch : list of int
            referring to the Reinvent runs which generated the data set
        active_inactive_list : list
            smiles divided in active and inactive list
        scores : list of int
            referring to xxx
        fingerprints : FingerprintContainerClass
            object which contains a name a list of fingerprints
        embedding : EmbeddingClass
            object which contains an np.array of dimensionally reduced fingerprints
        tanimoto_similarity : np.array
            contains scores, one for each target fingerprint

        Methods
        -------
        get_<attribute>:
            returns the attribute
        set_<attribute>:

        """

    def __init__(self, smiles_obj: Smiles,
                 name: str = "",
                 epoch: list = None,
                 active_inactive_list: list = None,
                 scores: list = [],
                 fingerprints: FingerprintContainer = None,
                 embedding: Embedding = None
                 ):

        self.name = name
        self.epoch = epoch
        self.active_inactive_list = active_inactive_list
        self.scores = scores
        self.smiles_obj = None
        self.set_smiles(smiles_obj)
        self.fingerprints = fingerprints
        self.embedding = embedding
        self.tanimoto_similarity = None

    def __repr__(self) -> str:
        return f"instance of ChemData with name: {self.name}," \
               f"epoch: {self.epoch}," \
               f"number scores: {len(self.scores)}," \
               f"smiles: {self.smiles_obj}," \
               f"fingerprint: {self.fingerprints}," \
               f"embedding: {self.embedding}"

    def __str__(self):
        return self.__repr__()

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str):
        self.name = name

    def get_epoch(self) -> list:
        return self.epoch

    def set_epoch(self, epoch: list):
        self.epoch = epoch

    def get_active_inactive_list(self) -> list:
        return self.active_inactive_list

    def set_active_inactive_list(self, active_inactive_list: list):
        self.active_inactive_list = active_inactive_list

    def get_scores(self) -> list:
        return self.scores

    def set_scores(self, scores: list):
        self.scores = scores

    def get_smiles(self) -> Smiles:
        return self.smiles_obj

    def set_smiles(self, smiles: Smiles):
        if isinstance(smiles, Smiles):
            self.smiles_obj = smiles
        else:
            raise ValueError(f"Unexpected value (type {type(smiles)}. Expected smiles object!")

    def get_fingerprints(self) -> FingerprintContainer:
        return self.fingerprints

    def set_fingerprints(self, fingerprints: FingerprintContainer):
        self.fingerprints = fingerprints

    def get_embedding(self) -> Embedding:
        return self.embedding

    def set_embedding(self, embedding: Embedding):
        self.embedding = embedding

    def get_tanimoto_similarity(self) -> np.array:
        return self.tanimoto_similarity

    def set_tanimoto_similarity(self, tanimoto_similarity: np.array):
        self.tanimoto_similarity = tanimoto_similarity
