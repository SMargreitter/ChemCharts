import pandas as pd
import plotly.express as px
import os
from chemcharts.core.container.chemdata import ChemData
from copy import deepcopy

from chemcharts.core.container.embedding import Embedding
from chemcharts.core.container.fingerprint import FingerprintContainer
from chemcharts.core.container.smiles import Smiles

from chemcharts.core.plots.hexag_plot import HexagonalPlot
from chemcharts.core.plots.scatter_boxplot_plot import ScatterBoxplotPlot
from chemcharts.core.plots.scatter_density_plot import ScatterDensityPlot
from chemcharts.core.plots.scatter_interactive import ScatterInteractivePlot
from chemcharts.core.plots.scatter_static_plot import ScatterStaticPlot
from chemcharts.core.plots.trisurf_plot import TrisurfPlot


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
    def _filter_epoch(chemcharts: ChemData, idx_value: list) -> ChemData:
        epoch_chemdata = ChemData(smiles_obj= Smiles(list(chemcharts.get_smiles())[idx_value]))
        epoch_chemdata.set_name(chemcharts.get_name())
        epoch_chemdata.set_epoch(chemcharts.get_epoch()[idx_value])
        epoch_chemdata.set_scores(chemcharts.get_scores()[idx_value])
        epoch_chemdata.set_fingerprints(chemcharts.get_fingerprints()[idx_value])
        epoch_chemdata.set_embedding(chemcharts.get_embedding()[idx_value])
        return epoch_chemdata

    @staticmethod
    def _path_update(old_path: str, epoch_id: int) -> str:
        os.path.split(os.path.abspath('/home/nutzer/Documents/Projects/ChemCharts/run_jupyter.txt'))
        path = "0000"
        updated_path = path [:-1] + str(epoch_id) + "_" + old_path + ".png"
        return updated_path
    #fill number with prefix/leading zeros

    def make_movie(self, chemcharts: ChemData, path: str):
        chemcharts = deepcopy(chemcharts)
        epochs = chemcharts.get_epoch()                           # [0,1,1,0,2,1,0]
        sorted_epochs = self._sort_epoch_list(epochs)              # [0,1,2]
        indices_list = self._find_indices(epochs, sorted_epochs)  # [[0,3,6], [1,2,5], [4]]
        for idx in range(len(sorted_epochs)):                                  #idx= #0 #1 #2
            for idx_value in indices_list[idx]:                                #idx_value= #0 #3 #6 || #1 #2 #5 || #4
                chemcharts_copy = deepcopy(chemcharts)
                epoch_chemdata = self._filter_epoch(chemcharts_copy, idx_value)
                updated_path = self._path_update(path, epoch_id=idx)

                self.plot(...)
            # find indices for epoch
            # filter epoch
            # path update
            # plot
        # make movie from paths

    @staticmethod
    def plot(chemdata: ChemData, path: str):
        raise NotImplemented("This method needs to be overloaded in a child class.")
