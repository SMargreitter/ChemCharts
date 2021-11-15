import pandas as pd
import plotly.express as px
from chemcharts.core.container.chemdata import ChemData
from copy import deepcopy


class BasePlot:
    def __init__(self):
        pass

    @staticmethod
    def _find_indices(values: list, x: int) -> list:
        buffer = []
        for idx in range(len(values)):
            if values[idx] == x:
                buffer.append(idx)
        return buffer

    @staticmethod
    def _filter_epoch(chemcharts: ChemData, epoch: int) -> ChemData:
        pass

    @staticmethod
    def _path_update(path: str, epoch_id: int) -> str:
        pass

    def make_movie(self, chemcharts: ChemData, path: str):
        chemcharts = deepcopy(chemcharts)
        epochs = chemcharts.get_epoch()
        epochs = list(set(epochs))
        epochs.sort()
                                                    # sorted_epoch has now all epochs in ascending order
        for epoch_id in epochs:
            # find indices for epoch
            # filter epoch
            # path update
            # plot
        # make movie from paths

    @staticmethod
    def plot(chemdata: ChemData, path: str):
        raise NotImplemented("This method needs to be overloaded in a child class.")
