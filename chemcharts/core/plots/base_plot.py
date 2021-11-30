import os
from chemcharts.core.container.chemdata import ChemData
from copy import deepcopy
import ffmpeg


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

    def make_movie(self, chemcharts: ChemData, movie_path: str, aggregate_epochs: bool = True):
        chemcharts = deepcopy(chemcharts)
        xlim = (min(chemcharts.get_embedding().np_array[:, 0]),
                max(chemcharts.get_embedding().np_array[:, 0]))
        ylim = (min(chemcharts.get_embedding().np_array[:, 1]),
                max(chemcharts.get_embedding().np_array[:, 1]))
        scorelim = (min(chemcharts.get_scores()), max(chemcharts.get_scores()))
        sorted_epochs = chemcharts.sort_epoch_list()
        updated_path_list = []
        total_number_observations = len(chemcharts.get_smiles())
        for idx in range(len(sorted_epochs)):
            if aggregate_epochs:
                epoch_chemdata = chemcharts.filter_epochs(epochs=[i for i in range(idx + 1)])
            else:
                epoch_chemdata = chemcharts.filter_epoch(epoch=idx)
            updated_snapshot_path = self._path_update_snapshot(ori_path=movie_path, epoch_id=idx)
            updated_path_list.append(updated_snapshot_path)
            self.plot(chemdata=epoch_chemdata,
                      path=updated_snapshot_path,
                      xlim=xlim,
                      ylim=ylim,
                      scorelim=scorelim,
                      total_number_observations=total_number_observations)

        path, file_name = os.path.split(os.path.abspath(movie_path))
        (
            ffmpeg
            .input(f"{path}/*.png", pattern_type='glob', framerate=5)
            .output(movie_path)
            .run()
        )

    @staticmethod
    def plot(chemdata: ChemData, path: str, xlim: tuple = None, ylim: tuple = None,
             scorelim: tuple = None, total_number_observations: int = None):
        raise NotImplemented("This method needs to be overloaded in a child class.")
