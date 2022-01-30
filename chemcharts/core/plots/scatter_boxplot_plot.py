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
        super(ScatterBoxplotPlot, self).plot(chemdata_list, parameters, settings)

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

            scatter_df = pd.DataFrame(
                {_PLE.UMAP_1: chemdata_list[idx].get_embedding().np_array[:, 0],
                 _PLE.UMAP_2: chemdata_list[idx].get_embedding().np_array[:, 1],
                 "z":
                    None if not chemdata_list[idx].get_scores() else chemdata_list[idx].get_scores(),
                 settings.get(_PE.SETTINGS_GROUP_NAME, _PE.SETTINGS_GROUP_NAME_DEFAULT):
                    None if not chemdata_list[idx].get_groups() else chemdata_list[idx].get_groups()})

            sns.set_context("talk", font_scale=0.5)

            g = sns.JointGrid(data=scatter_df,
                              x=_PLE.UMAP_1,
                              y=_PLE.UMAP_2,
                              xlim=xlim,
                              ylim=ylim,
                              hue=settings.get(_PE.SETTINGS_GROUP_NAME, _PE.SETTINGS_GROUP_NAME_DEFAULT),
                              palette="flare"
                              )

            plt.gcf().set_size_inches(settings.get(_PE.SETTINGS_FIG_SIZE, (6, 6)))
            g.plot_joint(sns.scatterplot)

            if settings.get(_PE.SETTINGS_BOXPLOT) is True:
                g.plot_marginals(sns.boxplot)

            plt.subplots_adjust(top=parameters.get(_PE.PARAMETERS_PLOT_ADJUST_TOP, 0.9))

            name = f"Dataset_{idx}" if chemdata_list[idx].get_name() == "" else chemdata_list[idx].get_name()
            plt.suptitle(name,
                         fontsize=parameters.get(_PE.PARAMETERS_PLOT_TITLE_FONTSIZE, 14))

            plt.savefig(temp_plots_path_list[idx],
                        format=settings.get(_PE.SETTINGS_FIG_FORMAT, 'png'),
                        dpi=settings.get(_PE.SETTINGS_FIG_DPI, _PE.SETTINGS_FIG_DPI_DEFAULT))

            plt.close("all")

        self._merge_multiple_plots(subplot_paths=temp_plots_path_list,
                                   merged_path=final_path,
                                   title=parameters.get(_PE.PARAMETERS_PLOT_TITLE, "Scatter Boxplot ChemCharts Plot"))
        self._clear_temp_dir(path=temp_folder_path)

