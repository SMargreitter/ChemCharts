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

    def plot(self, chemdata: ChemData, parameters: dict, settings: dict):
        xlim = parameters.get(_PE.PARAMETERS_XLIM, None)
        ylim = parameters.get(_PE.PARAMETERS_YLIM, None)
        path = settings.get(_PE.SETTINGS_PATH, None)
        scores_input = chemdata.get_scores() # update me
        score_name = chemdata.get_name()     # me too

        self._prepare_folder(path=path)

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
        scatter_df = pd.DataFrame({_PLE.UMAP_1: chemdata.get_embedding().np_array[:, 0],
                                   _PLE.UMAP_2: chemdata.get_embedding().np_array[:, 1],
                                   score_name: scores_input})

        sns.set_context("talk",
                        font_scale=0.5)

        plt.figure(settings.get(_PE.SETTINGS_FIG_SIZE, (17, 17)))

        sns.histplot(scatter_df[score_name],
                     element="step",
                     bins=parameters.get(_PE.PARAMETERS_BINS, 20),
                     stat="proportion",
                     color=parameters.get(_PE.PARAMETERS_PLOT_COLOR, "#d11d80"))

        plt.subplots_adjust(top=parameters.get(_PE.PARAMETERS_PLOT_ADJUST_TOP, 0.9))

        plt.suptitle(t=parameters.get(_PE.PARAMETERS_PLOT_TITLE, "Histogram ChemCharts Plot"),
                     fontsize=parameters.get(_PE.PARAMETERS_PLOT_TITLE_FONTSIZE, 18))

        # Setting axes ranges
        if xlim is not None or ylim is not None:
            print("Histogram plot does not support setting arbitrary axis limits.")
            plt.xlim(0, 1)      #TODO check me
            plt.ylim(0, 1)

        plt.savefig(path,
                    format=parameters.get(_PE.SETTINGS_FIG_FORMAT, 'png'),
                    dpi=parameters.get(_PE.SETTINGS_FIG_DPI, 300))

        plt.close("all")
