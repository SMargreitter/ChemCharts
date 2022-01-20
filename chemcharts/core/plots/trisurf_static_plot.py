from typing import List

import matplotlib.pyplot as plt

from chemcharts.core.container.chemdata import ChemData
from chemcharts.core.plots.base_plot import BasePlot

from chemcharts.core.utils.enums import PlottingEnum
from chemcharts.core.utils.enums import PlotLabellingEnum
_PE = PlottingEnum
_PLE = PlotLabellingEnum


class TrisurfStaticPlot(BasePlot):
    def __init__(self):
        super().__init__()

    def plot(self, chemdata_list: List[ChemData], parameters: dict, settings: dict):
        # lim setting
        xlim, ylim, scorelim = self._get_lims(chemdata_list=chemdata_list,
                                              parameters=parameters)

        # final path setting
        final_path = settings.get(_PE.SETTINGS_PATH, None)
        self._prepare_folder(path=final_path)

        # temp path setting
        temp_folder_path, temp_plots_path_list = self._generate_temp_paths(number_paths=len(chemdata_list))

        # loop over ChemData objects and generate plots
        for idx in range(len(chemdata_list)):

            ax = plt.axes(projection='3d')

            ax.plot_trisurf(chemdata_list[idx].get_embedding().np_array[:, 0],
                            chemdata_list[idx].get_embedding().np_array[:, 1],
                            chemdata_list[idx].get_scores(),
                            cmap=parameters.get(_PE.PARAMETERS_PLOT_COLOR, plt.get_cmap('twilight_shifted'))
                            )

            name = f"Dataset_{idx}" if chemdata_list[idx].get_name() == "" else chemdata_list[idx].get_name()
            ax.set_title(name)
            ax.set_xlabel(_PLE.UMAP_1)
            ax.set_ylabel(_PLE.UMAP_2)
            ax.set_zlabel(_PLE.SCORES)

            # setting axes ranges
            if xlim is not None:
                plt.xlim(xlim[0], xlim[1])
            if ylim is not None:
                plt.ylim(ylim[0], ylim[1])
            if scorelim is not None:
                ax.set_zlim(scorelim[0], scorelim[1])

            plt.savefig(temp_plots_path_list[idx],
                        format=settings.get(_PE.SETTINGS_FIG_FORMAT, 'png'),
                        dpi=settings.get(_PE.SETTINGS_FIG_DPI, _PE.SETTINGS_FIG_DPI_DEFAULT))

            plt.close("all")

        self._merge_multiple_plots(subplot_paths=temp_plots_path_list,
                                   merged_path=final_path,
                                   title=parameters.get(_PE.PARAMETERS_PLOT_TITLE, "Trisurf Static ChemCharts Plot"))
        self._clear_temp_dir(path=temp_folder_path)
