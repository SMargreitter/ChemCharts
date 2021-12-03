import matplotlib.pyplot as plt

from chemcharts.core.container.chemdata import ChemData
from chemcharts.core.plots.base_plot import BasePlot


class ScatterStaticPlot(BasePlot):
    def __init__(self):
        super().__init__()

    def plot(self, chemdata: ChemData, parameters: dict, settings: dict):
        xlim = parameters["xlim"]
        ylim = parameters["ylim"]
        scorelim = parameters["scorelim"]
        path = settings["path"]

        self._prepare_folder(path=path)

        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')

        plt.gcf().set_size_inches((15, 15))

        ax.scatter(chemdata.get_embedding().np_array[:, 0],
                   chemdata.get_embedding().np_array[:, 1],
                   zs=chemdata.get_scores(),
                   s=1)

        ax.set_title("Scatter Static ChemCharts Plot")
        ax.set_xlabel('UMAP 1')
        ax.set_ylabel('UMAP 2')
        ax.set_zlabel('Scores')

        # setting axes ranges
        if xlim is not None:
            plt.xlim(xlim[0], xlim[1])
        if ylim is not None:
            plt.ylim(ylim[0], ylim[1])
        if scorelim is not None:
            ax.set_zlim(scorelim[0], scorelim[1])

        plt.savefig(path)
        plt.close(fig)
