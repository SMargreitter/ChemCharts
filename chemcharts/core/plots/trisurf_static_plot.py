import matplotlib.pyplot as plt

from chemcharts.core.container.chemdata import ChemData
from chemcharts.core.plots.base_plot import BasePlot

from chemcharts.core.utils.enums import PlottingEnum
from chemcharts.core.utils.enums import PlotLabellingEnum
_PE = PlottingEnum
_PLE = PlotLabellingEnum


class TrisurfStaticPlot(BasePlot):
    def __init__(self):
        super().__init__()

    def plot(self, chemdata: ChemData, parameters: dict, settings: dict):
        xlim = parameters.get(_PE.PARAMETERS_XLIM, None)
        ylim = parameters.get(_PE.PARAMETERS_YLIM, None)
        path = settings.get(_PE.SETTINGS_PATH, None)
        scorelim = parameters.get(_PE.PARAMETERS_SCORELIM, None)

        self._prepare_folder(path=path)

        fig = plt.figure(figsize=(14, 9))
        ax = plt.axes(projection='3d')

        cmap = plt.get_cmap('twilight_shifted')
        ax.plot_trisurf(chemdata.get_embedding().np_array[:, 0],
                        chemdata.get_embedding().np_array[:, 1],
                        chemdata.get_scores(),
                        cmap=cmap
                        )

        # Adding labels
        ax.set_title("Trisurf Static ChemCharts Plot")
        ax.set_xlabel(_PLE.UMAP_1)
        ax.set_ylabel(_PLE.UMAP_2)
        ax.set_zlabel(_PLE.SCORES)

        # Setting axes ranges
        if xlim is not None:
            plt.xlim(xlim[0], xlim[1])
        if ylim is not None:
            plt.ylim(ylim[0], ylim[1])
        if scorelim is not None:
            ax.set_zlim(scorelim[0], scorelim[1])

        plt.savefig(path)
        plt.close(fig)
