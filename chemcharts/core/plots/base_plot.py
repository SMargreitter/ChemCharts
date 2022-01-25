import os
import tempfile
import shutil
from typing import List, Tuple

import ffmpeg
from copy import deepcopy
from PIL import Image, ImageFont, ImageDraw
from chemcharts.core.container.chemdata import ChemData
from chemcharts.core.utils.enums import PlottingEnum, MovieEnum

_PE = PlottingEnum
_ME = MovieEnum


def _check_score_input(chemdata_list: List[ChemData], plot_type: str) -> bool:
    # check whether there is a score input
    for idx in range(len(chemdata_list)):
        if not chemdata_list[idx].get_scores():
            print(f"Input Warning: {plot_type}_plot generation without score input not possible! "
                  "(only hexagonal and scatter_boxplot plots can be generated without scores)")
            return False
    return True


def _check_epoch_input(chemdata_list: List[ChemData]) -> bool:
    # check whether there is an epoch input
    for idx in range(len(chemdata_list)):
        if not chemdata_list[idx].get_epochs():
            print(f"Input Warning: Multiple plots and movie generation without epoch input not possible!")
            return False
    return True


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
    def _merge_chemdata_list(chemdata_list: List[ChemData]) -> ChemData:
        chemdata_buffer = ChemData()
        for chemdata in chemdata_list:
            chemdata_buffer = chemdata_buffer + chemdata
        return chemdata_buffer

    @staticmethod
    def _get_lims(chemdata_list: List[ChemData], parameters: dict) -> Tuple[Tuple, Tuple, Tuple]:
        total_xlims = []
        total_ylims = []
        total_scorelims = []
        for idx in range(len(chemdata_list)):
            total_xlims += [None] if parameters.get(_PE.PARAMETERS_XLIM, None) is None else parameters[_PE.PARAMETERS_XLIM]
            total_ylims += [None] if parameters.get(_PE.PARAMETERS_YLIM, None) is None else parameters[_PE.PARAMETERS_YLIM]
            total_scorelims += [None] if parameters.get(_PE.PARAMETERS_SCORELIM, None) is None else parameters[_PE.PARAMETERS_SCORELIM]
        xlim = None if None in total_xlims else (min(total_xlims), max(total_xlims))
        ylim = None if None in total_ylims else (min(total_ylims), max(total_ylims))
        scorelim = None if None in total_scorelims else (min(total_scorelims), max(total_scorelims))
        return xlim, ylim, scorelim

    @staticmethod
    def _generate_temp_paths(number_paths: int) -> Tuple[str, List[str]]:
        tempdir = tempfile.mkdtemp()
        file_path_list = []
        for idx_path in range(number_paths):
            _, file_path = tempfile.mkstemp(prefix=str(idx_path),
                                            dir=tempdir)
            file_path_list.append(file_path)
        return tempdir, file_path_list

    @staticmethod
    def _clear_temp_dir(path: str):
        if os.path.isdir(path):
            shutil.rmtree(path)

    @staticmethod
    def _merge_multiple_plots(subplot_paths: List[str], merged_path: str, title: str):
        # get list of image, widths and heights
        image_list = [Image.open(x) for x in subplot_paths]
        widths_list, heights_list = zip(*(i.size for i in image_list))
        width, _ = image_list[0].size
        number_plots = len(subplot_paths)

        total_width = sum(widths_list)
        max_height = max(heights_list)+200

        # create new image
        new_im = Image.new('RGB', size=(total_width, max_height), color="white")

        # add images to new image
        x_offset = 0
        for im in image_list:
            # x dimension changes with every image,y dimension always stays 0
            new_im.paste(im, (x_offset, 150))
            # update x dimension
            x_offset += im.size[0]

        font_file = "/usr/share/fonts/truetype/freefont/FreeSerif.ttf"
        if os.path.isfile(font_file):
            draw = ImageDraw.Draw(new_im)
            if number_plots == 1:
                font_size = int(130 / 2700 * width)
            else:
                font_size = int(48 / 2700 * total_width)

            font = ImageFont.truetype(font_file, size=font_size)

            if number_plots == 1:
                draw.text((width/4.5, 30), title, (0, 0, 0), font=font)
            else:
                draw.text((total_width/2.5, 30), title, (0, 0, 0), font=font)

        # save new merged image to path
        new_im.save(merged_path)

    def generate_movie(self,
                       chemdata_list: List[ChemData],
                       parameters: dict = {},
                       settings: dict = {},
                       aggregate_epochs: bool = True):
        epoch_input_result = _check_epoch_input(chemdata_list)

        # checks whether _check_epoch_input function returns 'True'
        if epoch_input_result:

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
            self._prepare_folder(path=settings[_ME.SETTINGS_MOVIE_PATH])
            xlim = (min(chemdata_list.get_embedding().np_array[:, 0]),
                    max(chemdata_list.get_embedding().np_array[:, 0]))
            ylim = (min(chemdata_list.get_embedding().np_array[:, 1]),
                    max(chemdata_list.get_embedding().np_array[:, 1]))
            scorelim = (min(chemdata_list.get_scores()),
                        max(chemdata_list.get_scores()))
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

                # extract current epoch if flag is true in parameters
                # TODO: refactor that, as it is only used for contour generation in hexagonal_plot yet
                use_current_epoch = parameters.get(_ME.PARAMETERS_USE_CURRENT_EPOCH, False)
                current_chemdata = None if not use_current_epoch else chemdata_list.filter_epoch(epoch=idx)

                updated_snapshot_path = self._path_update_snapshot(ori_path=settings[_ME.SETTINGS_MOVIE_PATH],
                                                                   epoch_id=idx)
                updated_path_list.append(updated_snapshot_path)

                # plot generation
                self.plot(chemdata_list=[epoch_chemdata],
                          parameters={_PE.PARAMETERS_XLIM: xlim,
                                      _PE.PARAMETERS_YLIM: ylim,
                                      _PE.PARAMETERS_SCORELIM: scorelim,
                                      _PE.PARAMETERS_CURRENT_CHEMDATA: current_chemdata,
                                      _PE.PARAMETERS_TOTAL_CHEMDATA: total_chemdata},
                          settings={_PE.SETTINGS_VIEW: "",
                                    _PE.SETTINGS_PATH: updated_snapshot_path}
                          )

            # movie generation
            path, file_name = os.path.split(os.path.abspath(settings[_ME.SETTINGS_MOVIE_PATH]))
            ending = file_name[-4:].lower()
            if ending == _ME.ENDING_GIF:
                _, tmp_path_mp4 = tempfile.mkstemp(suffix=".mp4")
                (
                    ffmpeg
                        .input(f"{path}/*.png", pattern_type='glob', framerate=5)
                        .output(tmp_path_mp4)
                        .global_args("-y")
                        .run()
                )
                command = ' '.join(["ffmpeg",
                                    "-y",
                                    "-i", tmp_path_mp4,
                                    "-r 15",
                                    '-vf "scale=512:-1,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse"',
                                    settings[_ME.SETTINGS_MOVIE_PATH]])
                result = os.system(command)
            elif ending == _ME.ENDING_MP4:
                (
                    ffmpeg
                    .input(f"{path}/*.png", pattern_type='glob', framerate=5)
                    .output(settings[_ME.SETTINGS_MOVIE_PATH])
                    .run()
                )
            else:
                raise ValueError(f"Only .gif and .mp4 is supported.")

    # error message
    def plot(self, chemdata_list: List[ChemData], parameters: dict, settings: dict):
        raise NotImplemented("This method needs to be overloaded in a child class.")
