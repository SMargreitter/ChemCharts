from copy import deepcopy
from typing import List

import numpy as np
import pandas as pd

from chemcharts.core.container.embedding import Embedding
from chemcharts.core.container.fingerprint import FingerprintContainer
from chemcharts.core.container.smiles import Smiles


class ChemData:
    """
        This class represents information about molecules for generating plots.

        ...

        Attributes (required)
        ----------
        smiles_obj : Smiles
            object contains a list of Smiles objects (eg [O=C1c2ccccc2C(=O)N1CCC1=Cc2ccccc2CCC1, ...])

        Attributes (optional)
        ----------
        name : str
            should reflect the input data
        epoch : list of int
            referring to the Reinvent runs which generated the data set
        groups : list of int
            referring to groups for coloring plots
        active_inactive_list : list
            smiles divided in active and inactive list
        values : dataframe
            pandas dataframe containing columns with values e.g. total_scores, raw_dockstream, ...
        fingerprints : FingerprintContainer
            object which contains a name a list of fingerprints
        embedding : Embedding
            object which contains an np.array of dimensionally reduced fingerprints
        tanimoto_similarity : np.array
            contains scores, one for each target fingerprint

        Methods
        -------
        sort_epoch_list:
            returns an ascending list of unique epochs
        find_epoch_indices <sorted_epochs: list>:
            returns a list of the epoch indices
        filter_epoch <epoch: int>:
            returns a ChemData object with the object belonging to a specific epoch
        filter_epochs <epochs: list>:
            returns a ChemData object for a specific epoch
    """

    def __init__(self, smiles_obj: Smiles = None,
                 name: str = "",
                 epochs: list = None,
                 groups: list = None,
                 active_inactive_list: list = None,
                 values: pd.DataFrame = None,
                 fingerprints: FingerprintContainer = None,
                 embedding: Embedding = None,
                 tanimoto_similarity: np.array = None
                 ):

        # set defaults
        self.name = name
        self.epochs = [] if epochs is None else epochs
        self.groups = [] if groups is None else groups
        self.active_inactive_list = [] if active_inactive_list is None else active_inactive_list
        self.values = pd.DataFrame() if values is None else values
        self.smiles_obj = Smiles() if smiles_obj is None else smiles_obj
        self.fingerprints = FingerprintContainer("") if fingerprints is None else fingerprints
        self.embedding = Embedding() if embedding is None else embedding
        self.tanimoto_similarity = np.empty((0, 2), float) if tanimoto_similarity is None else tanimoto_similarity

    def __repr__(self) -> str:
        return f"instance of ChemData with name: {self.name}," \
               f"epoch: {self.epochs}," \
               f"group: {self.groups}," \
               f"values: {self.values.columns}," \
               f"smiles: {self.smiles_obj}," \
               f"fingerprint: {self.fingerprints}," \
               f"embedding: {self.embedding}"

    def __str__(self):
        return self.__repr__()

    def __add__(self, obj):
        copy_self = deepcopy(self)
        obj = deepcopy(obj)
        copy_self.set_epochs(copy_self.epochs + obj.epochs)
        copy_self.set_groups(copy_self.groups + obj.groups)
        copy_self.set_active_inactive_list(copy_self.active_inactive_list + obj.active_inactive_list)
        copy_self.set_values(pd.concat([copy_self.values, obj.values]))
        copy_self.set_smiles(copy_self.smiles_obj + obj.smiles_obj)
        copy_self.set_fingerprints(copy_self.fingerprints + obj.fingerprints)
        copy_self.set_embedding(copy_self.embedding + obj.embedding)
        copy_self.set_tanimoto_similarity(np.empty((0, 2), float))
        return copy_self

    def sort_epoch_list(self) -> List[int]:
        # sort epoch list and casts it to integers
        sorted_epochs = list(set(self.get_epochs()))
        sorted_epochs.sort()
        sorted_epochs = [int(e) for e in sorted_epochs]
        return sorted_epochs

    def find_epoch_indices(self, sorted_epochs: List[int]) -> List[List[int]]:
        # return list of epoch indices
        epoch_indices_list = []
        epochs = self.get_epochs()
        for ep in sorted_epochs:
            buffer = []
            for idx in range(len(epochs)):
                if epochs[idx] == ep:
                    buffer.append(idx)
            epoch_indices_list.append(buffer)
        return epoch_indices_list

    def filter_epochs(self, epochs: List[int]):
        # return a chemdata with observations of MULTIPLE epochs
        multiple_epoch_chemdata = ChemData()
        for idx in epochs:
            multiple_epoch_chemdata = multiple_epoch_chemdata + self.filter_epoch(epoch=idx)
        return multiple_epoch_chemdata

    def filter_epoch(self, epoch: int):
        # return a chemdata with observations of ONE epoch only
        copy_chemdata = deepcopy(self)
        sorted_epochs = copy_chemdata.sort_epoch_list()
        epoch_indices = copy_chemdata.find_epoch_indices(sorted_epochs)[epoch]
        epoch_chemdata = \
            ChemData(smiles_obj=Smiles([copy_chemdata.get_smiles()[i] for i in epoch_indices]),
                     name=f"epoch_{epoch}_chemdata",
                     epochs=[] if not copy_chemdata.get_epochs()
                     else [copy_chemdata.get_epochs()[i] for i in epoch_indices],
                     groups=[] if not copy_chemdata.get_groups()
                     else [copy_chemdata.get_groups()[i] for i in epoch_indices],
                     values=None if copy_chemdata.get_values() is None
                     else copy_chemdata.get_values().iloc[epoch_indices],
                     fingerprints=FingerprintContainer(name=f"epoch_{epoch}_fps",
                                                       fingerprint_list=[copy_chemdata.get_fingerprints()[i] for i in
                                                                         epoch_indices]),
                     embedding=Embedding() if copy_chemdata.get_embedding().np_array is None else Embedding(np.vstack([copy_chemdata.get_embedding()[i] for i in epoch_indices])))
        return epoch_chemdata

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str):
        self.name = name

    def get_epochs(self) -> list:
        return self.epochs

    def set_epochs(self, epochs: list):
        self.epochs = epochs

    def get_groups(self) -> list:
        return self.groups

    def set_groups(self, groups: list):
        self.groups = groups

    def get_active_inactive_list(self) -> list:
        return self.active_inactive_list

    def set_active_inactive_list(self, active_inactive_list: list):
        self.active_inactive_list = active_inactive_list

    def get_values(self) -> pd.DataFrame:
        return self.values

    def get_values_by_column(self, column_name: str) -> List[float]:
        return self.values[column_name]

    def set_values(self, values: pd.DataFrame):
        self.values = values

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
