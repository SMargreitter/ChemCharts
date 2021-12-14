from typing import List

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

    def plot(self, chemdata_list: List[ChemData], parameters: dict, settings: dict):
        if isinstance(chemdata_list, list):
            print("Function does not support multiple input objects (yet).")
            chemdata_list = chemdata_list[0]

        xlim = parameters.get(_PE.PARAMETERS_XLIM, None)
        ylim = parameters.get(_PE.PARAMETERS_YLIM, None)
        path = settings.get(_PE.SETTINGS_PATH, None)
        current_chemdata = parameters.get(_PE.PARAMETERS_CURRENT_CHEMDATA, None)
        total_chemdata = parameters.get(_PE.PARAMETERS_TOTAL_CHEMDATA, chemdata_list)
        gridsize = parameters.get(_PE.PARAMETERS_GRIDSIZE, None)

        self._prepare_folder(path=path)

        extent = (xlim[0], xlim[1], ylim[0], ylim[1]) if xlim is not None else None

        if gridsize is None:
            x_bins = int(min(_freedman_diaconis_bins(total_chemdata.get_embedding().np_array[:, 0]), 50))
            y_bins = int(min(_freedman_diaconis_bins(total_chemdata.get_embedding().np_array[:, 1]), 50))
            gridsize = int(np.mean([x_bins, y_bins]))

        hb = plt.hexbin(x=total_chemdata.get_embedding().np_array[:, 0],
                        y=total_chemdata.get_embedding().np_array[:, 1],
                        color=parameters.get(_PE.PARAMETERS_PLOT_COLOR, "#4CB391"),
                        gridsize=gridsize)

        # TODO: implement the "glow" to indicate current additions
        #       see 2nd solution: https://stackoverflow.com/questions/65469173/matplotlib-add-border-around-group-of-bins-with-most-frequent-values-in-hexbin
        if current_chemdata is not None:
            print("GOFORIT")
            sns.jointplot(x=current_chemdata.get_embedding().np_array[:, 0],
                          y=current_chemdata.get_embedding().np_array[:, 1],
                          xlim=xlim,
                          ylim=ylim,
                          joint_kws={"gridsize": gridsize,
                                     "zorder": -2,
                                     "lw": 5,
                                     "vmin": 0,
                                     "vmax": hb.get_array().max()},
                          kind="hex",
                          extent=extent,
                          color="black"
                          )

        sns.jointplot(x=chemdata_list.get_embedding().np_array[:, 0],
                      y=chemdata_list.get_embedding().np_array[:, 1],
                      xlim=xlim,
                      ylim=ylim,
                      joint_kws={"gridsize": gridsize,
                                 "vmin": 0,
                                 "zorder": -1,
                                 "lw": 2,
                                 "vmax": hb.get_array().max()},
                      kind="hex",
                      extent=extent,
                      color=parameters.get(_PE.PARAMETERS_PLOT_COLOR, "#4CB391")
                      )

        plt.subplots_adjust(top=parameters.get(_PE.PARAMETERS_PLOT_ADJUST_TOP, 0.9))

        plt.suptitle(t=parameters.get(_PE.PARAMETERS_PLOT_TITLE, "Hexagonal ChemCharts Plot"),
                     fontsize=parameters.get(_PE.PARAMETERS_PLOT_TITLE_FONTSIZE, 14))

        plt.savefig(path,
                    format=settings.get(_PE.SETTINGS_FIG_FORMAT, 'png'),
                    dpi=settings.get(_PE.SETTINGS_FIG_DPI, 100))

        plt.close()
