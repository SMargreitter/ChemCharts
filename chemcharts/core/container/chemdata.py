import numpy as np
import pandas as pd

from chemcharts.core.container.embedding import Embedding
from chemcharts.core.container.fingerprint import FingerprintContainer
from chemcharts.core.container.smiles import Smiles


class ChemData:
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
