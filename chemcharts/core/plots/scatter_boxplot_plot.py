from typing import List

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from chemcharts.core.container.chemdata import ChemData
from chemcharts.core.plots.base_plot import BasePlot

from chemcharts.core.utils.enums import PlottingEnum
from chemcharts.core.utils.enums import PlotLabellingEnum
_PE = PlottingEnum
_PLE = PlotLabellingEnum


class ScatterBoxplotPlot(BasePlot):
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

            scatter_df = pd.DataFrame({_PLE.UMAP_1: chemdata_list[idx].get_embedding().np_array[:, 0],
                                       _PLE.UMAP_2: chemdata_list[idx].get_embedding().np_array[:, 1],
                                       "z": chemdata_list[idx].get_scores()})

            sns.set_context("talk", font_scale=0.5)

            g = sns.JointGrid(data=scatter_df,
                              x=_PLE.UMAP_1,
                              y=_PLE.UMAP_2,
                              xlim=xlim,
                              ylim=ylim
                              )

            g.plot_joint(sns.scatterplot)
            g.plot_marginals(sns.boxplot)

            # TODO set figsize with user input?
            plt.subplots_adjust(top=parameters.get(_PE.PARAMETERS_PLOT_ADJUST_TOP, 0.9))

            name = f"Dataset_{idx}" if chemdata_list[idx].get_name() == "" else chemdata_list[idx].get_name()
            plt.suptitle(name,
                         fontsize=parameters.get(_PE.PARAMETERS_PLOT_TITLE_FONTSIZE, 14))

            plt.savefig(temp_plots_path_list[idx],
                        format=settings.get(_PE.SETTINGS_FIG_FORMAT, 'png'),
                        dpi=settings.get(_PE.SETTINGS_FIG_DPI, 250))

            plt.close("all")

        self._merge_multiple_plots(subplot_paths=temp_plots_path_list,
                                   merged_path=final_path)
        self._clear_temp_dir(path=temp_folder_path)

