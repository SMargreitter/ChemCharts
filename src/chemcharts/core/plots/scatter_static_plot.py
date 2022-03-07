from typing import List

import matplotlib.pyplot as plt

from chemcharts.core.container.chemdata import ChemData
from chemcharts.core.plots.base_plot import BasePlot, _check_value_input
from chemcharts.core.utils.value_functions import generate_value

from chemcharts.core.utils.enums import PlottingEnum
from chemcharts.core.utils.enums import PlotLabellingEnum
_PE = PlottingEnum
_PLE = PlotLabellingEnum


class ScatterStaticPlot(BasePlot):
    def __init__(self):
        super().__init__()

    def plot(self, chemdata_list: List[ChemData], parameters: dict, settings: dict):
        # base class call
        super(ScatterStaticPlot, self).plot(chemdata_list, parameters, settings)

        # checks whether there is a score input
        value_input_result = _check_value_input(chemdata_list, "Scatter_static")

        # checks whether there are multiple input objects
        if value_input_result:      # checks whether _check_value_input function returns 'True'
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

                value_column, value_name = generate_value(chemdata_list=chemdata_list,
                                                          parameters=parameters,
                                                          idx=idx)

                plt.figure(figsize=(settings.get(_PE.SETTINGS_FIG_SIZE, (5, 5))))
                ax = plt.axes(projection='3d')

                ax.scatter(chemdata_list[idx].get_embedding().np_array[:, 0],
                           chemdata_list[idx].get_embedding().np_array[:, 1],
                           zs=value_column,
                           s=parameters.get(_PE.PARAMETERS_PLOT_S, 1),
                           color=parameters.get(_PE.PARAMETERS_PLOT_COLOR, "#0000ff"))

                name = f"Dataset_{idx}" if chemdata_list[idx].get_name() == "" else chemdata_list[idx].get_name()
                ax.set_title(name)
                ax.set_xlabel(_PLE.UMAP_1)
                ax.set_ylabel(_PLE.UMAP_2)
                ax.set_zlabel(value_name)

                # setting axes ranges
                if xlim is not None:
                    plt.xlim(xlim[0], xlim[1])
                if ylim is not None:
                    plt.ylim(ylim[0], ylim[1])
                if valuelim is not None:
                    ax.set_zlim(valuelim[0], valuelim[1])

                plt.savefig(temp_plots_path_list[idx],
                            format=settings.get(_PE.SETTINGS_FIG_FORMAT, 'png'),
                            dpi=settings.get(_PE.SETTINGS_FIG_DPI, _PE.SETTINGS_FIG_DPI_DEFAULT))

                plt.close("all")

            self._merge_multiple_plots(subplot_paths=temp_plots_path_list,
                                       merged_path=final_path,
                                       title=parameters.get(_PE.PARAMETERS_PLOT_TITLE, "Scatter Static ChemCharts Plot"))
            self._clear_temp_dir(path=temp_folder_path)
