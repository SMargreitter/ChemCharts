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

    @staticmethod
    def _make_plain_plot(scatter_df, xlim, ylim, parameters: dict):
        g = sns.JointGrid(data=scatter_df,
                          x=_PLE.UMAP_1,
                          y=_PLE.UMAP_2,
                          xlim=xlim,
                          ylim=ylim,
                          palette=parameters.get(_PE.PARAMETERS_PLOT_COLOR, "flare")
                          )
        return g

    @staticmethod
    def _make_score_plot(scatter_df, xlim, ylim, parameters: dict, vmin: float, vmax: float):
        g = sns.JointGrid(data=scatter_df,
                          x=_PLE.UMAP_1,
                          y=_PLE.UMAP_2,
                          xlim=xlim,
                          ylim=ylim,
                          hue=scatter_df["Scores"],
                          hue_norm=None if vmin is None or vmax is None else (vmin, vmax),
                          palette=parameters.get(_PE.PARAMETERS_PLOT_COLOR, "flare")
                          )

        # Make space for the colorbar
        g.fig.subplots_adjust(left=0.250)

        # Get a mappable object with the same colormap as the data
        points = plt.scatter([], [], c=[], vmin=vmin, vmax=vmax, cmap=parameters.get(_PE.PARAMETERS_PLOT_COLOR, "flare"))

        # Add axes for colorbar
        cbaxes = g.fig.add_axes([0.02, 0.15, 0.03, 0.6])

        # Draw the colorbar
        g.fig.colorbar(points, cax=cbaxes)

        return g

    @staticmethod
    def _make_group_plot(scatter_df, xlim, ylim, parameters: dict):
        g = sns.JointGrid(data=scatter_df,
                          x=_PLE.UMAP_1,
                          y=_PLE.UMAP_2,
                          xlim=xlim,
                          ylim=ylim,
                          hue=parameters.get(_PE.PARAMETERS_GROUP_LEGEND_NAME, _PE.PARAMETERS_GROUP_LEGEND_NAME_DEFAULT),
                          palette=parameters.get(_PE.PARAMETERS_PLOT_COLOR, "flare")
                          )
        return g

    def plot(self, chemdata_list: List[ChemData], parameters: dict, settings: dict):
        # base class call
        super(ScatterBoxplotPlot, self).plot(chemdata_list, parameters, settings)

        # lim setting
        xlim, ylim, scorelim = self._get_lims(chemdata_list=chemdata_list,
                                              parameters=parameters)

        # final path setting
        final_path = settings.get(_PE.SETTINGS_PATH, None)
        self._prepare_folder(path=final_path)

        # temp path setting
        temp_folder_path, temp_plots_path_list = self._generate_temp_paths(number_paths=len(chemdata_list))

        # calculates vmin and vmax if not set, otherwise uses min and max values of scores
        new_list = []
        vmin = None
        vmax = None
        for chemdata_object in chemdata_list:
            new_list.extend(chemdata_object.get_scores())
        if len(new_list) > 0:
            vmin = parameters.get(_PE.PARAMETERS_VMIN, min(new_list))
            vmax = parameters.get(_PE.PARAMETERS_VMAX, max(new_list))

        # loop over ChemData objects and generate plots
        for idx in range(len(chemdata_list)):

            scatter_df = pd.DataFrame(
                {_PLE.UMAP_1: chemdata_list[idx].get_embedding().np_array[:, 0],
                 _PLE.UMAP_2: chemdata_list[idx].get_embedding().np_array[:, 1]})

            sns.set_context("talk", font_scale=0.5)

            mode = parameters.get(_PE.PARAMETERS_MODE, "plain")
            if mode == "plain":
                scatter_df.insert(2,
                                  "Scores",
                                  None if not chemdata_list[idx].get_scores()
                                  else chemdata_list[idx].get_scores(),
                                  allow_duplicates=False)
                g = self._make_plain_plot(scatter_df, xlim, ylim, parameters)
            elif mode == "scores":
                scatter_df.insert(2,
                                  "Scores",
                                  None if not chemdata_list[idx].get_scores()
                                  else chemdata_list[idx].get_scores(),
                                  allow_duplicates=False)
                g = self._make_score_plot(scatter_df, xlim, ylim, parameters, vmin, vmax)
            elif mode == "groups":
                scatter_df.insert(2,
                                  parameters.get(_PE.PARAMETERS_GROUP_LEGEND_NAME, _PE.PARAMETERS_GROUP_LEGEND_NAME_DEFAULT),
                                  None if not chemdata_list[idx].get_groups()
                                  else chemdata_list[idx].get_groups(),
                                  allow_duplicates=False)
                g = self._make_group_plot(scatter_df, xlim, ylim, parameters)
            else:
                raise ValueError(f"Please choose a plot mode (plain, scores or groups)")

            plt.gcf().set_size_inches(settings.get(_PE.SETTINGS_FIG_SIZE, (6, 6)))
            g.plot_joint(sns.scatterplot)

            if mode == "scores":
                legend = g.ax_joint.legend().remove()

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

