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

    def _make_plain_plot(self, scatter_df, xlim, ylim):
        g = sns.JointGrid(data=scatter_df,
                          x=_PLE.UMAP_1,
                          y=_PLE.UMAP_2,
                          xlim=xlim,
                          ylim=ylim,
                          hue="Scores",
                          palette="flare"
                          )
        return g

    def _make_score_plot(self, scatter_df, xlim, ylim, parameters):
        g = sns.JointGrid(data=scatter_df,
                          x=_PLE.UMAP_1,
                          y=_PLE.UMAP_2,
                          xlim=xlim,
                          ylim=ylim,
                          hue="Scores",
                          palette="flare"
                          )

        # cmap = sns.diverging_palette(240, 10, l=65, center="dark", as_cmap=True)

        # Make space for the colorbar
        g.fig.subplots_adjust(right=.92)

        # Get a mappable object with the same colormap as the data
        points = plt.scatter([], [], c=[], vmin=0, vmax=1, cmap="flare")

        # Draw the colorbar
        g.fig.colorbar(points)

        return g

    def _make_group_plot(self, scatter_df, xlim, ylim, parameters):
        g = sns.JointGrid(data=scatter_df,
                          x=_PLE.UMAP_1,
                          y=_PLE.UMAP_2,
                          xlim=xlim,
                          ylim=ylim,
                          hue=parameters.get(_PE.PARAMETERS_GROUP_LEGEND_NAME, _PE.PARAMETERS_GROUP_LEGEND_NAME_DEFAULT),
                          palette="flare"
                          )
        return g

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
                 _PLE.UMAP_2: chemdata_list[idx].get_embedding().np_array[:, 1]})

            sns.set_context("talk", font_scale=0.5)

            if parameters.get(_PE.PARAMETERS_MODE) == "plain":
                scatter_df.assign(Scores=[None if not chemdata_list[idx].get_scores()
                                          else chemdata_list[idx].get_scores()])
                g = self._make_plain_plot(scatter_df, xlim, ylim)
            elif parameters.get(_PE.PARAMETERS_MODE) == "scores":
                scatter_df.assign(Scores=[None if not chemdata_list[idx].get_scores()
                                          else chemdata_list[idx].get_scores()])
                g = self._make_score_plot(scatter_df, xlim, ylim, parameters)
            elif parameters.get(_PE.PARAMETERS_MODE) == "groups":
                scatter_df.assign(Groups=[None if not chemdata_list[idx].get_groups()
                                          else chemdata_list[idx].get_groups()])
                g = self._make_group_plot(scatter_df, xlim, ylim, parameters)
            else:
                raise ValueError(f"Please choose a mode (plain, score or groups)")

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

