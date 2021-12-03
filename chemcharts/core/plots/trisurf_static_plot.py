import matplotlib.pyplot as plt

from chemcharts.core.container.chemdata import ChemData
from chemcharts.core.plots.base_plot import BasePlot

from chemcharts.core.utils.enums import PlottingEnum
_PE = PlottingEnum


class TrisurfStaticPlot(BasePlot):
    def __init__(self):
        super().__init__()

    def plot(self, chemdata: ChemData, parameters: dict, settings: dict):
        xlim = parameters[_PE.PARAMETERS_XLIM]
        ylim = parameters[_PE.PARAMETERS_YLIM]
        scorelim = parameters[_PE.PARAMETERS_SCORELIM]
        path = settings[_PE.SETTINGS_PATH]

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
        ax.set_xlabel('UMAP 1')
        ax.set_ylabel('UMAP 2')
        ax.set_zlabel('Scores')

        # Setting axes ranges
        if xlim is not None:
            plt.xlim(xlim[0], xlim[1])
        if ylim is not None:
            plt.ylim(ylim[0], ylim[1])
        if scorelim is not None:
            ax.set_zlim(scorelim[0], scorelim[1])

        plt.savefig(path)
        plt.close(fig)
