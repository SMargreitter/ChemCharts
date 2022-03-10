from typing import List

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from chemcharts.core.container.chemdata import ChemData
from chemcharts.core.plots.base_plot import BasePlot
from chemcharts.core.utils.enums import PlotLabellingEnum
from chemcharts.core.utils.enums import PlottingEnum

_PE = PlottingEnum
_PLE = PlotLabellingEnum


class ScatterBoxplotPlot(BasePlot):
    def __init__(self):
        super().__init__()

    @staticmethod
    def _make_plain_plot(scatter_df, xlim, ylim, parameters: dict):
        c_input = parameters.get(_PE.PARAMETERS_PLOT_COLOR, '#4368ff')
        color_input = list([c_input])

        g = sns.JointGrid(data=scatter_df,
                          x=_PLE.UMAP_1,
                          y=_PLE.UMAP_2,
                          xlim=xlim,
                          ylim=ylim,
                          hue=[1 for _ in range(len(scatter_df))],
                          palette=sns.color_palette(color_input, n_colors=1)
                          )
        return g

    @staticmethod
    def _make_value_plot(scatter_df, xlim, ylim, parameters: dict, vmin: float, vmax: float):
        value_name = parameters.get(_PE.PARAMETERS_VALUENAME)
        hue = value_name if value_name is not None else print("Warning: Value name needs to be set for the"
                                                              "value plot type.")

        g = sns.JointGrid(data=scatter_df,
                          x=_PLE.UMAP_1,
                          y=_PLE.UMAP_2,
                          xlim=xlim,
                          ylim=ylim,
                          hue=hue,
                          hue_norm=None if vmin is None or vmax is None else (vmin, vmax),
                          palette=parameters.get(_PE.PARAMETERS_PLOT_COLOR, "flare")
                          )

        # Make space for the colorbar
        g.fig.subplots_adjust(left=0.250)

        # Get a mappable object with the same colormap as the data
        points = plt.scatter([], [], c=[], vmin=vmin, vmax=vmax, cmap=parameters.get(_PE.PARAMETERS_PLOT_COLOR, "mako"))

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
                          palette=parameters.get(_PE.PARAMETERS_PLOT_COLOR, "mako")
                          )
        return g

    def plot(self, chemdata_list: List[ChemData], parameters: dict, settings: dict):
        # base class call
        super(ScatterBoxplotPlot, self).plot(chemdata_list, parameters, settings)

        # TODO either remove or fix custom palette
        # color palette/cmap when list of hex colors are to be accepted
        #cmap, color = self._coloring(parameters=parameters)

        # lim setting
        xlim, ylim, valuelim = self._get_lims(chemdata_list=chemdata_list,
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

            mode = parameters.get(_PE.PARAMETERS_MODE, "plain")
            if mode == "plain":
                g = self._make_plain_plot(scatter_df, xlim, ylim, parameters)
            elif mode == "value":
                # extract column name (if set and available in values dataframe)
                value_column_name = parameters.get(_PE.PARAMETERS_VALUECOLUMN, None)
                if value_column_name is None or value_column_name not in list(
                        chemdata_list[0].get_values().columns):
                    raise ValueError("Can only plot in value mode when both values dataframe and "
                                     "column name are provided and column is present in dataframe.")

                # calculates vmin and vmax if not set (using min and max values of value)
                new_list = []
                vmin, vmax = parameters.get(_PE.PARAMETERS_VALUELIM, [None, None])
                if vmin is None or vmax is None:
                    for chemdata_object in chemdata_list:
                        new_list.extend(chemdata_object.get_values_by_column(value_column_name))
                    vmin, vmax = [min(new_list), max(new_list)]

                scatter_df.insert(2,
                                  parameters.get(_PE.PARAMETERS_VALUENAME, "Value"),
                                  chemdata_list[idx].get_values_by_column(value_column_name),
                                  allow_duplicates=False)
                g = self._make_value_plot(scatter_df, xlim, ylim, parameters, vmin, vmax)
            elif mode == "groups":
                scatter_df.insert(2,
                                  parameters.get(_PE.PARAMETERS_GROUP_LEGEND_NAME,
                                                 _PE.PARAMETERS_GROUP_LEGEND_NAME_DEFAULT),
                                  chemdata_list[idx].get_groups(),
                                  allow_duplicates=False)
                g = self._make_group_plot(scatter_df, xlim, ylim, parameters)
            else:
                raise ValueError(f"Please choose a plot mode (plain, value or groups)")

            plt.gcf().set_size_inches(settings.get(_PE.SETTINGS_FIG_SIZE, (6, 6)))
            g.plot_joint(sns.scatterplot)

            if mode == "value" or mode == "plain":
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

