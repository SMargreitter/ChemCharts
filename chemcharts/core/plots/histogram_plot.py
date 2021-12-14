from typing import List

import matplotlib
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from chemcharts.core.container.chemdata import ChemData
from chemcharts.core.plots.base_plot import BasePlot

from chemcharts.core.utils.enums import PlottingEnum
from chemcharts.core.utils.enums import PlotLabellingEnum
_PE = PlottingEnum
_PLE = PlotLabellingEnum


class HistogramPlot(BasePlot):
    def __init__(self):
        super().__init__()

    def plot(self, chemdata_list: List[ChemData], parameters: dict, settings: dict):
        path = settings.get(_PE.SETTINGS_PATH, None)
        self._prepare_folder(path=path)

        # fig settings
        max_columns = 3
        len_chemdata = len(chemdata_list)
        n_rows = int((len_chemdata - 1) / max_columns) + 1
        n_cols = min(len_chemdata, max_columns)
        figsize = settings.get(_PE.SETTINGS_FIG_SIZE, (17*n_cols, 17*n_rows))

        # create fig
        fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
        fig.suptitle('Vertically stacked subplots')
        for idx in range(len(chemdata_list)):
            xlim = parameters.get(_PE.PARAMETERS_XLIM, None)
            ylim = parameters.get(_PE.PARAMETERS_YLIM, None)

            scores_input = chemdata_list[idx].get_scores()
            score_name = chemdata_list[idx].get_name()

            """      
            if selection == "tanimoto_similarity":
                scores_input = chemdata.get_tanimoto_similarity()
                score_name = "Tanimoto Similarity"
            elif selection == "scores":
                scores_input = chemdata.get_scores()
                score_name = "Scores"
            else:
                raise ValueError(f"Selection input: {selection} is not as expected.")
            """

            scatter_df = pd.DataFrame({_PLE.UMAP_1: chemdata_list[idx].get_embedding().np_array[:, 0],
                                       _PLE.UMAP_2: chemdata_list[idx].get_embedding().np_array[:, 1],
                                       score_name: scores_input})

            sns.set_context("talk",
                            font_scale=0.5)

            # deal with axes (array if multiple input, otherwise not) issue
            if isinstance(axes, np.ndarray):
                selected_axis = axes[int(idx / max_columns), idx % max_columns]
            else:
                selected_axis = axes

            sns.histplot(scatter_df[score_name],
                         element="step",
                         bins=parameters.get(_PE.PARAMETERS_BINS, 20),
                         stat="proportion",
                         kde=True,
                         color=parameters.get(_PE.PARAMETERS_PLOT_COLOR, "#d11d80"),
                         ax=selected_axis)

            # Setting axes ranges
            # For this plot only x and y axis ranges from 0 to 1 make sense
            if xlim is not None or ylim is not None:
                print("Histogram plot does not support setting arbitrary axis limits.")
            plt.xlim(0, 1)
            plt.ylim(0, 1)

        plt.subplots_adjust(top=parameters.get(_PE.PARAMETERS_PLOT_ADJUST_TOP, 0.9))

        plt.suptitle(t=parameters.get(_PE.PARAMETERS_PLOT_TITLE, "Histogram ChemCharts Plot"),
                     fontsize=parameters.get(_PE.PARAMETERS_PLOT_TITLE_FONTSIZE, 18))

        plt.savefig(path,
                    format=parameters.get(_PE.SETTINGS_FIG_FORMAT, 'png'),
                    dpi=parameters.get(_PE.SETTINGS_FIG_DPI, 300))

        plt.close("all")
