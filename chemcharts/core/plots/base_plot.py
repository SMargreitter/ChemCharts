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

    def make_movie(self, chemcharts: ChemData, movie_path: str):
        chemcharts = deepcopy(chemcharts)
        sorted_epochs = chemcharts.sort_epoch_list()
        indices_list = chemcharts.find_epoch_indices(sorted_epochs)
        updated_path_list = []
        for idx in range(len(sorted_epochs)):
            epoch_chemdata = chemcharts.filter_epoch(epoch=idx, epoch_indices_list=indices_list[idx])
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
