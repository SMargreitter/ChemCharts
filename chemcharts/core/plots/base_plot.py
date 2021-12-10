import os
import shutil
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
        path, file_name = os.path.split(os.path.abspath(ori_path))
        stripped_file_name = file_name.split(".", 1)[0]
        updated_file_name = f"{stripped_file_name}.png"
        updated_path = f'{path}/{epoch_id:04}_{updated_file_name}'
        return updated_path

    @staticmethod
    def _prepare_folder(path: str):
        path, _ = os.path.split(os.path.abspath(path))
        if not os.path.isdir(path):
            os.mkdir(path)

    def generate_movie(self, chemcharts: ChemData, movie_path: str, aggregate_epochs: bool = True):
        len_epochs = len(chemcharts.get_epochs())
        len_embedding = len(chemcharts.get_embedding().np_array[:, 0])
        if len_epochs != len_embedding:
            raise ValueError(f"Length of epochs ({len_epochs}) not equal embedding length ({len_embedding}), movie generation with clustered data not supported.")

        chemcharts = deepcopy(chemcharts)
        self._prepare_folder(path=movie_path)
        xlim = (min(chemcharts.get_embedding().np_array[:, 0]),
                max(chemcharts.get_embedding().np_array[:, 0]))
        ylim = (min(chemcharts.get_embedding().np_array[:, 1]),
                max(chemcharts.get_embedding().np_array[:, 1]))
        scorelim = (min(chemcharts.get_scores()), max(chemcharts.get_scores()))

        sorted_epochs = chemcharts.sort_epoch_list()
        updated_path_list = []
        total_number_observations = len(chemcharts.get_smiles())
        total_chemcharts = chemcharts
        for idx in range(len(sorted_epochs)):
            if aggregate_epochs:
                epoch_chemdata = chemcharts.filter_epochs(epochs=[i for i in range(idx + 1)])
            else:
                epoch_chemdata = chemcharts.filter_epoch(epoch=idx)
            updated_snapshot_path = self._path_update_snapshot(ori_path=movie_path, epoch_id=idx)
            updated_path_list.append(updated_snapshot_path)
            self.plot(chemdata=epoch_chemdata,
                      parameters={_PE.PARAMETERS_XLIM: xlim,
                                  _PE.PARAMETERS_YLIM: ylim,
                                  _PE.PARAMETERS_SCORELIM: scorelim,
                                  _PE.PARAMETERS_TOTAL_NUMBER_OBSERVATIONS: total_number_observations,
                                  _PE.PARAMETERS_TOTAL: total_chemcharts},
                      settings={_PE.SETTINGS_VIEW: "",
                                _PE.SETTINGS_PATH: updated_snapshot_path}
                      )

        path, file_name = os.path.split(os.path.abspath(movie_path))
        (
            ffmpeg
            .input(f"{path}/*.png", pattern_type='glob', framerate=5)
            .output(movie_path)
            .run()
        )

    def plot(self, chemdata: ChemData, parameters: dict, settings: dict):
        raise NotImplemented("This method needs to be overloaded in a child class.")
