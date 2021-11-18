import pandas as pd
import plotly.express as px
import os
from chemcharts.core.container.chemdata import ChemData
from copy import deepcopy
import numpy as np
import ffmpeg

from chemcharts.core.container.embedding import Embedding
from chemcharts.core.container.fingerprint import FingerprintContainer
from chemcharts.core.container.smiles import Smiles


class BasePlot:
    def __init__(self):
        pass

    @staticmethod
    def _sort_epoch_list(epochs: list) -> list:
        sorted_epochs = list(set(epochs))
        sorted_epochs.sort()
        return sorted_epochs

    @staticmethod
    def _find_indices(epochs: list, sorted_epochs: list) -> list:
        indices_list = []
        for ep in sorted_epochs:
            buffer = []
            for idx in range(len(epochs)):
                if epochs[idx] == ep:
                    buffer.append(idx)
            indices_list.append(buffer)
        return indices_list

    @staticmethod
    def _filter_epoch(chemcharts: ChemData, epoch: int, epoch_indices_list: list) -> ChemData:
        epoch_chemdata = \
            ChemData(smiles_obj=Smiles([chemcharts.get_smiles()[i] for i in epoch_indices_list]),
                     name=f"epoch_{epoch}_chemdata",
                     epoch=[chemcharts.get_epoch()[i] for i in epoch_indices_list],
                     scores=[chemcharts.get_scores()[i] for i in epoch_indices_list],
                     fingerprints=FingerprintContainer(name=f"epoch_{epoch}_fps",
                                                       fingerprint_list=[chemcharts.get_fingerprints()[i] for i in
                                                                         epoch_indices_list]),
                     embedding=Embedding(np.vstack([chemcharts.get_embedding()[i] for i in epoch_indices_list])))
        return epoch_chemdata

    @staticmethod
    def _path_update_snapshot(ori_path: str, epoch_id: int) -> str:
        path, file_name = os.path.split(os.path.abspath(ori_path))
        updated_path = f'{path}/{epoch_id:04}_{file_name}'
        # TODO replace everthing after the last '.' by ".png"
        return updated_path

    def make_movie(self, chemcharts: ChemData, movie_path: str):
        chemcharts = deepcopy(chemcharts)
        epochs = chemcharts.get_epoch()                                               # [0,1,1,0,2,1,0]
        sorted_epochs = self._sort_epoch_list(epochs)                                 # [0,1,2]
        indices_list = self._find_indices(epochs, sorted_epochs)                      # [[0,3,6], [1,2,5], [4]]
        updated_path_list = []
        for idx in range(len(sorted_epochs)):                                         #idx= #0 #1 #2
            chemcharts_copy = deepcopy(chemcharts)
            epoch_chemdata = self._filter_epoch(chemcharts=chemcharts_copy, epoch=idx, epoch_indices_list=indices_list[idx])    #indices_list= #[0,3,6] #[1,2,5] #[4]
            updated_snapshot_path = self._path_update_snapshot(ori_path=movie_path, epoch_id=idx)
            updated_path_list.append(updated_snapshot_path)
            self.plot(chemdata=epoch_chemdata, path=updated_snapshot_path)

        path, file_name = os.path.split(os.path.abspath(movie_path))
        (
            ffmpeg
            .input(f"{path}/*.png", pattern_type='glob', framerate=1)
            .output(movie_path)
            .run()
        )

    @staticmethod
    def plot(chemdata: ChemData, path: str):
        raise NotImplemented("This method needs to be overloaded in a child class.")
