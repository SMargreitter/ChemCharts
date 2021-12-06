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

    def plot(self, chemdata: ChemData, parameters: dict, settings: dict):
        xlim = parameters.get(_PE.PARAMETERS_XLIM, None)
        ylim = parameters.get(_PE.PARAMETERS_YLIM, None)
        path = settings.get(_PE.SETTINGS_PATH, None)

        self._prepare_folder(path=path)

        scatter_df = pd.DataFrame({_PLE.UMAP_1: chemdata.get_embedding().np_array[:, 0],
                                   _PLE.UMAP_2: chemdata.get_embedding().np_array[:, 1],
                                   "z": chemdata.get_scores()})

        sns.set_context("talk", font_scale=0.5)
        plt.figure(figsize=(17, 17))
        g = sns.JointGrid(data=scatter_df,
                          x=_PLE.UMAP_1,
                          y=_PLE.UMAP_2,
                          xlim=xlim,
                          ylim=ylim
                          )
        g.plot_joint(sns.scatterplot)
        g.plot_marginals(sns.boxplot)

        plt.subplots_adjust(top=0.9)
        plt.suptitle('Scatter Boxplot ChemCharts Plot', fontsize=14)

        plt.savefig(path, format='png', dpi=150)
        plt.close("all")
