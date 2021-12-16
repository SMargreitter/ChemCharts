import os
from typing import List, Tuple

import ffmpeg
from copy import deepcopy

from chemcharts.core.container.chemdata import ChemData

from chemcharts.core.utils.enums import PlottingEnum

_PE = PlottingEnum


class BasePlot:
    def __init__(self):
        pass

    @staticmethod
    def _path_update_snapshot(ori_path: str, epoch_id: int) -> str:
        # update path with ".png" filename as well as epoch reference
        path, file_name = os.path.split(os.path.abspath(ori_path))
        stripped_file_name = file_name.split(".", 1)[0]
        updated_file_name = f"{stripped_file_name}.png"
        updated_path = f'{path}/{epoch_id:04}_{updated_file_name}'
        return updated_path

    @staticmethod
    def _prepare_folder(path: str):
        # generate folder if not yet available
        path, _ = os.path.split(os.path.abspath(path))
        if not os.path.isdir(path):
            os.mkdir(path)

    @staticmethod
    def _get_lims(chemdata_list: List[ChemData], parameters: dict) -> Tuple[Tuple, Tuple, Tuple]:
        total_xlims = []
        total_ylims = []
        total_scorelims = []
        for idx in range(len(chemdata_list)):
            total_xlims += list(parameters.get(_PE.PARAMETERS_XLIM, [None]))
            total_ylims += list(parameters.get(_PE.PARAMETERS_YLIM, [None]))
            total_scorelims += list(parameters.get(_PE.PARAMETERS_SCORELIM, [None]))
        xlim = None if None in total_xlims else (min(total_xlims), max(total_xlims))
        ylim = None if None in total_ylims else (min(total_ylims), max(total_ylims))
        scorelim = None if None in total_scorelims else (min(total_scorelims), max(total_scorelims))
        return xlim, ylim, scorelim

    def generate_movie(self, chemdata_list: List[ChemData], movie_path: str, aggregate_epochs: bool = True):
        # movie function does not (yet) support multiple dataset input
        if isinstance(chemdata_list, list):
            print("Function does not (yet) support multiple input objects.")
            chemdata_list = chemdata_list[0]

        # error message
        len_epochs = len(chemdata_list.get_epochs())
        len_embedding = len(chemdata_list.get_embedding().np_array[:, 0])
        if len_epochs != len_embedding:
            raise ValueError(f"Length of epochs ({len_epochs}) not equal embedding length ({len_embedding}),"
                             f"movie generation with clustered data not supported.")

        # preparation
        chemdata_list = deepcopy(chemdata_list)
        self._prepare_folder(path=movie_path)
        xlim = (min(chemdata_list.get_embedding().np_array[:, 0]),
                max(chemdata_list.get_embedding().np_array[:, 0]))
        ylim = (min(chemdata_list.get_embedding().np_array[:, 1]),
                max(chemdata_list.get_embedding().np_array[:, 1]))
        scorelim = (min(chemdata_list.get_scores()), max(chemdata_list.get_scores()))
        sorted_epochs = chemdata_list.sort_epoch_list()
        updated_path_list = []
        total_chemdata = chemdata_list

        # epoch_chemdata generation
        for idx in range(len(sorted_epochs)):
            if aggregate_epochs:
                # list comprehension range is index +1, to get the actual epoch indices,
                # e.g. idx=0 will lead to epoch 0 selected
                epoch_chemdata = chemdata_list.filter_epochs(epochs=[i for i in range(idx + 1)])
            else:
                # useful when big batch sizes, not exposed at the moment!
                epoch_chemdata = chemdata_list.filter_epoch(epoch=idx)

            current_chemdata = chemdata_list.filter_epoch(epoch=idx)
            updated_snapshot_path = self._path_update_snapshot(ori_path=movie_path, epoch_id=idx)
            updated_path_list.append(updated_snapshot_path)

            # plot generation
            self.plot(chemdata_list=epoch_chemdata,
                      parameters={_PE.PARAMETERS_XLIM: xlim,
                                  _PE.PARAMETERS_YLIM: ylim,
                                  _PE.PARAMETERS_SCORELIM: scorelim,
                                  _PE.PARAMETERS_CURRENT_CHEMDATA: current_chemdata,
                                  _PE.PARAMETERS_TOTAL_CHEMDATA: total_chemdata},
                      settings={_PE.SETTINGS_VIEW: "",
                                _PE.SETTINGS_PATH: updated_snapshot_path}
                      )

        # movie generation
        path, file_name = os.path.split(os.path.abspath(movie_path))
        (
            ffmpeg
            .input(f"{path}/*.png", pattern_type='glob', framerate=5)
            .output(movie_path)
            .run()
        )

    # error message
    def plot(self, chemdata_list: List[ChemData], parameters: dict, settings: dict):
        raise NotImplemented("This method needs to be overloaded in a child class.")
