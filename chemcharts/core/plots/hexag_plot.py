import seaborn as sns
import matplotlib.pyplot as plt

from chemcharts.core.container.chemdata import ChemData
from chemcharts.core.plots.base_plot import BasePlot

from chemcharts.core.utils.enums import PlottingEnum
_PE = PlottingEnum


class HexagonalPlot(BasePlot):
    def __init__(self):
        super().__init__()

    def plot(self, chemdata: ChemData, parameters: dict, settings: dict):
        xlim = parameters.get(_PE.PARAMETERS_XLIM, None)
        ylim = parameters.get(_PE.PARAMETERS_YLIM, None)
        path = settings.get(_PE.SETTINGS_PATH, None)

        self._prepare_folder(path=path)

        extent = (xlim[0], xlim[1], ylim[0], ylim[1]) if xlim is not None else None

        sns.jointplot(x=chemdata.get_embedding().np_array[:, 0],
                      y=chemdata.get_embedding().np_array[:, 1],
                      xlim=xlim,
                      ylim=ylim,
                      joint_kws={"gridsize": 20},
                      kind="hex",
                      extent=extent,
                      color="#4CB391")

        plt.subplots_adjust(top=0.9)
        plt.suptitle(parameters.get(_PE.PARAMETERS_TITLE, "Hexagonal ChemCharts Plot"), fontsize=14)

        plt.savefig(path)
        plt.close()
