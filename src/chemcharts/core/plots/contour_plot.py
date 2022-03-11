from typing import List

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from scipy.interpolate import griddata

from chemcharts.core.container.chemdata import ChemData
from chemcharts.core.plots.base_plot import BasePlot
from chemcharts.core.utils.value_functions import generate_value

from chemcharts.core.utils.enums import PlottingEnum
from chemcharts.core.utils.enums import PlotLabellingEnum
_PE = PlottingEnum
_PLE = PlotLabellingEnum


class ContourPlot(BasePlot):
    def __init__(self):
        super().__init__()

    @staticmethod
    def _make_2d_contour_plot(scatter_df, name, xlim, ylim, parameters: dict):
        # setting axes ranges and dataset title
        if xlim is not None:
            plt.xlim(xlim[0], xlim[1])
        if ylim is not None:
            plt.ylim(ylim[0], ylim[1])
        plt.title(name)

        # set seaborn style
        sns.set_style("white")

        g = sns.kdeplot(x=scatter_df[_PLE.UMAP_1],
                        y=scatter_df[_PLE.UMAP_2],
                        bw_adjust=parameters.get(_PE.PARAMETERS_BW_ADJUST, 1),
                        cmap=parameters.get(_PE.PARAMETERS_PLOT_COLOR, None),
                        shade=parameters.get(_PE.PARAMETERS_SHADE, None),
                        thresh=parameters.get(_PE.PARAMETERS_THRESH, 0.05))

        return g

    @staticmethod
    def _make_3d_contour_plot(scatter_df, name, xlim, ylim, valuelim, value_name, parameters: dict):
        x = scatter_df[_PLE.UMAP_1]
        y = scatter_df[_PLE.UMAP_2]
        z = scatter_df[value_name]

        # target grid to interpolate to
        mesh_closeness = parameters.get(_PE.PARAMETERS_MESH_CLOSENESS, 2)
        xi = np.arange(xlim[0], xlim[1], mesh_closeness)
        yi = np.arange(ylim[0], ylim[1], mesh_closeness)
        xi, yi = np.meshgrid(xi, yi)

        # interpolate
        zi = griddata((x, y), z, (xi, yi), method='linear')

        # generate plot
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        ax.plot_surface(xi,
                        yi,
                        zi,
                        cmap=parameters.get(_PE.PARAMETERS_PLOT_COLOR, "magma"),
                        lw=0.5,
                        rstride=1,
                        cstride=1)

        # set axes title and dataset title
        ax.set_title(name)
        ax.set_xlabel(_PLE.UMAP_1)
        ax.set_ylabel(_PLE.UMAP_2)
        ax.set_zlabel(value_name)

        # set axes ranges
        if xlim is not None:
            plt.xlim(xlim[0], xlim[1])
        if ylim is not None:
            plt.ylim(ylim[0], ylim[1])
        if valuelim is not None:
            ax.set_zlim(valuelim[0], valuelim[1])

        return ax

    def plot(self, chemdata_list: List[ChemData], parameters: dict, settings: dict):
        # base class call
        super(ContourPlot, self).plot(chemdata_list, parameters, settings)

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
            if len(chemdata_list) > 1:
                name = f"Dataset_{idx}" if chemdata_list[idx].get_name() == "" else chemdata_list[idx].get_name()
            else:
                name = None

            if chemdata_list[idx].get_values().empty or parameters.get(_PE.PARAMETERS_VALUECOLUMN) is None:
                scatter_df = pd.DataFrame({_PLE.UMAP_1: chemdata_list[idx].get_embedding().np_array[:, 0],
                                           _PLE.UMAP_2: chemdata_list[idx].get_embedding().np_array[:, 1],
                                           })

                g = self._make_2d_contour_plot(scatter_df, name, xlim, ylim, parameters)
            else:
                value_column, value_name = generate_value(chemdata_list=chemdata_list,
                                                          parameters=parameters,
                                                          idx=idx)

                scatter_df = pd.DataFrame({_PLE.UMAP_1: chemdata_list[idx].get_embedding().np_array[:, 0],
                                           _PLE.UMAP_2: chemdata_list[idx].get_embedding().np_array[:, 1],
                                           value_name: value_column})

                g = self._make_3d_contour_plot(scatter_df, name, xlim, ylim, valuelim, value_name, parameters)

            plt.savefig(temp_plots_path_list[idx],
                        format=settings.get(_PE.SETTINGS_FIG_FORMAT, 'png'),
                        dpi=settings.get(_PE.SETTINGS_FIG_DPI, _PE.SETTINGS_FIG_DPI_DEFAULT))

            plt.close("all")

        self._merge_multiple_plots(subplot_paths=temp_plots_path_list,
                                   merged_path=final_path,
                                   title=parameters.get(_PE.PARAMETERS_PLOT_TITLE, "Contour ChemCharts Plot"))
        self._clear_temp_dir(path=temp_folder_path)
