import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from seaborn.distributions import _freedman_diaconis_bins

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
        total = parameters.get(_PE.PARAMETERS_TOTAL, chemdata)

        self._prepare_folder(path=path)

        extent = (xlim[0], xlim[1], ylim[0], ylim[1]) if xlim is not None else None

    #    x_bins = min(_freedman_diaconis_bins(grid.x), 50)
    #    y_bins = min(_freedman_diaconis_bins(grid.y), 50)
    #    gridsize = int(np.mean([x_bins, y_bins]))

        hb = plt.hexbin(x=total.get_embedding().np_array[:, 0],
                        y=total.get_embedding().np_array[:, 1],
                        color="#4CB391")

        sns.jointplot(x=chemdata.get_embedding().np_array[:, 0],
                      y=chemdata.get_embedding().np_array[:, 1],
                      xlim=xlim,
                      ylim=ylim,
                      joint_kws={"gridsize": 20,
                                 "C": np.ones_like(chemdata.get_embedding().np_array[:, 1], dtype=np.float) /
                                      hb.get_array().max(),
                                 "reduce_C_function": np.sum},
                      kind="hex",
                      extent=extent,
                      color="#4CB391"
                      )

        plt.subplots_adjust(top=0.9)
        plt.suptitle(parameters.get(_PE.PARAMETERS_TITLE, "Hexagonal ChemCharts Plot"), fontsize=14)

        plt.savefig(path)
        plt.close()

"""
    def plot(self, chemdata: ChemData, parameters: dict, settings: dict):
        xlim = parameters.get(_PE.PARAMETERS_XLIM, None)
        ylim = parameters.get(_PE.PARAMETERS_YLIM, None)
        path = settings.get(_PE.SETTINGS_PATH, None)
        total = parameters.get(_PE.PARAMETERS_TOTAL, chemdata)
#        if xlim and ylim is not None:
#            print("x:", xlim[0])
#            print("x:", xlim[1])
#            print("y:", ylim[0])
#            print("y:", ylim[1])

        self._prepare_folder(path=path)

        plt.subplot(111)
        hb = plt.hexbin(x=total.get_embedding().np_array[:, 0],
                        y=total.get_embedding().np_array[:, 1],
                        cmap=plt.cm.YlOrRd_r)

        plt.cla()
        plt.hexbin(x=chemdata.get_embedding().np_array[:, 0],
                   y=chemdata.get_embedding().np_array[:, 1],
                   C=np.ones_like(chemdata.get_embedding().np_array[:, 1], dtype=np.float) / hb.get_array().max(),
                   cmap=plt.cm.YlOrRd_r,
                   reduce_C_function=np.sum)

        plt.axis([xlim[0], xlim[1], ylim[0], ylim[1]]) if xlim is not None else None
        cb = plt.colorbar()

        plt.subplots_adjust(top=0.9)
        plt.suptitle(parameters.get(_PE.PARAMETERS_TITLE, "Hexagonal ChemCharts Plot"), fontsize=14)

        plt.savefig(path)
        plt.close()
"""
"""
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
"""