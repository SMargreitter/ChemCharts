from typing import List

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from chemcharts.core.container.chemdata import ChemData
from chemcharts.core.plots.base_plot import BasePlot, _check_value_input
from chemcharts.core.utils.value_functions import generate_value

from chemcharts.core.utils.enums import PlottingEnum
from chemcharts.core.utils.enums import PlotLabellingEnum
_PE = PlottingEnum
_PLE = PlotLabellingEnum


class HistogramPlot(BasePlot):
    def __init__(self):
        super().__init__()

    def plot(self, chemdata_list: List[ChemData], parameters: dict, settings: dict):
        # no warning message for multiple chemdata object inputs since normalisation
        # for xlim and ylim is here anyways applied

        # checks whether there is a value input
        value_input_result = _check_value_input(chemdata_list, "Histogram")

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

            max_columns = 3

            # loop over ChemData objects and generate plots
            for idx in range(len(chemdata_list)):
                fig, axs = plt.subplots()

                value_column, value_name = generate_value(chemdata_list=chemdata_list,
                                                          parameters=parameters,
                                                          idx=idx)

                # TODO fix tanimoto
                """   
                # include tanimoto_similarity   
                if selection == "tanimoto_similarity":
                    value_input = chemdata.get_tanimoto_similarity()
                    value_name = "Tanimoto Similarity"
                elif selection == "value":
                    value_input = chemdata.get_values()
                    value_name = parameters.get(_PE.V
                else:
                    raise ValueError(f"Selection input: {selection} is not as expected.")
                """

                # generate data frame
                scatter_df = pd.DataFrame({_PLE.UMAP_1: chemdata_list[idx].get_embedding().np_array[:, 0],
                                           _PLE.UMAP_2: chemdata_list[idx].get_embedding().np_array[:, 1],
                                           value_name: value_column})

                sns.set_context("talk",
                                font_scale=0.5)

                # deal with axs issue (array if multiple input, otherwise not)
                if isinstance(axs, np.ndarray):
                    row_pos = int(idx / max_columns)
                    col_pos = idx % max_columns

                    # makes sure that array is 2D, even if only one row
                    axs = np.atleast_2d(axs)
                    selected_axis = axs[row_pos, col_pos]
                else:
                    selected_axis = axs

                # generate seaborn histplot
                sns.histplot(scatter_df[value_name],
                             element="step",
                             bins=parameters.get(_PE.PARAMETERS_BINS, 20),
                             stat="proportion",
                             kde=True,
                             color=parameters.get(_PE.PARAMETERS_PLOT_COLOR, "#d11d80"),
                             ax=selected_axis)

                # Setting axs ranges (for this plot only x and y axis ranges from 0 to 1 make sense)
                if xlim is not None or ylim is not None:
                    print("Histogram plot does not support setting arbitrary axis limits.")
                plt.xlim(0, 1)
                plt.ylim(0, 1)

                plt.gcf().set_size_inches(settings.get(_PE.SETTINGS_FIG_SIZE, (7, 7)))
                plt.subplots_adjust(top=parameters.get(_PE.PARAMETERS_PLOT_ADJUST_TOP, 0.9))
                plt.xlabel(parameters.get(_PE.PARAMETERS_VALUENAME, "Value"), fontsize=10)

                name = f"Dataset_{idx}" if chemdata_list[idx].get_name() == "" else chemdata_list[idx].get_name()
                plt.suptitle(name,
                             fontsize=parameters.get(_PE.PARAMETERS_PLOT_TITLE_FONTSIZE, 14))

                plt.savefig(temp_plots_path_list[idx],
                            format=settings.get(_PE.SETTINGS_FIG_FORMAT, 'png'),
                            dpi=settings.get(_PE.SETTINGS_FIG_DPI, _PE.SETTINGS_FIG_DPI_DEFAULT))

                plt.close("all")

            self._merge_multiple_plots(subplot_paths=temp_plots_path_list,
                                       merged_path=final_path,
                                       title=parameters.get(_PE.PARAMETERS_PLOT_TITLE, "Histogram ChemCharts Plot"))
            self._clear_temp_dir(path=temp_folder_path)
