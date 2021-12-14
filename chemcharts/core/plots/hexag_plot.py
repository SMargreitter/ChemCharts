from typing import List

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from seaborn.distributions import _freedman_diaconis_bins

from chemcharts.core.container.chemdata import ChemData
from chemcharts.core.plots.base_plot import BasePlot

from chemcharts.core.utils.enums import PlottingEnum
_PE = PlottingEnum


def hexLines(a=None,i=None,off=[0,0]):
    '''regular hexagon segment lines as `(xy1,xy2)` in clockwise
    order with points in line sorted top to bottom
    for irregular hexagon pass both `a` (vertical) and `i` (horizontal)'''
    if a is None: a = 2 / np.sqrt(3) * i;
    if i is None: i = np.sqrt(3) / 2 * a;
    h  = a / 2
    xy = np.array([ [ [ 0, a], [ i, h] ],
                    [ [ i, h], [ i,-h] ],
                    [ [ i,-h], [ 0,-a] ],
                    [ [-i,-h], [ 0,-a] ], #flipped
                    [ [-i, h], [-i,-h] ], #flipped
                    [ [ 0, a], [-i, h] ]  #flipped
                  ])
    return xy+off


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

        if current_chemdata is not None:
            hb_current = plt.hexbin(x=current_chemdata.get_embedding().np_array[:, 0],
                                    y=current_chemdata.get_embedding().np_array[:, 1],
                                    color=parameters.get(_PE.PARAMETERS_PLOT_COLOR, "#4CB391"),
                                    gridsize=gridsize,
                                    extent=extent)

        hb = plt.hexbin(x=total_chemdata.get_embedding().np_array[:, 0],
                        y=total_chemdata.get_embedding().np_array[:, 1],
                        color=parameters.get(_PE.PARAMETERS_PLOT_COLOR, "#4CB391"),
                        gridsize=gridsize,
                        extent=extent)

        # inspired by 2nd solution from here:
        # https://stackoverflow.com/questions/65469173/matplotlib-add-border-around-group-of-bins-with-most-frequent-values-in-hexbin

        sns.jointplot(x=chemdata_list.get_embedding().np_array[:, 0],
                      y=chemdata_list.get_embedding().np_array[:, 1],
                      xlim=xlim,
                      ylim=ylim,
                      joint_kws={"gridsize": gridsize,
                                 "vmin": 0,
                                 "lw": 1,
                                 "vmax": hb.get_array().max()},
                      kind="hex",
                      extent=extent,
                      color=parameters.get(_PE.PARAMETERS_PLOT_COLOR, "#4CB391")
                      )
        if current_chemdata is not None:
            # get hexagon centers that should be highlighted
            verts = hb_current.get_offsets()
            cnts = hb_current.get_array()
            highl = verts[cnts > 0 * cnts.max()]

            # create hexagon lines
            a = ((verts[0, 1] - verts[1, 1]) / 3).round(6)
            i = ((verts[1:, 0] - verts[:-1, 0]) / 2).round(6)
            i = i[i > 0][0]
            lines = np.concatenate([hexLines(a, i, off) for off in highl])

            # select contour lines and draw
            uls, c = np.unique(lines.round(4), axis=0, return_counts=True)
            for l in uls[c == 1]:
                data = l.transpose()
                sns.lineplot(x=data[0], y=data[1], lw=2, scalex=False, scaley=False, color="black")

        plt.subplots_adjust(top=parameters.get(_PE.PARAMETERS_PLOT_ADJUST_TOP, 0.9))
        plt.suptitle(t=parameters.get(_PE.PARAMETERS_PLOT_TITLE, "Hexagonal ChemCharts Plot"),
                     fontsize=parameters.get(_PE.PARAMETERS_PLOT_TITLE_FONTSIZE, 14))

        plt.savefig(path,
                    format=settings.get(_PE.SETTINGS_FIG_FORMAT, 'png'),
                    dpi=settings.get(_PE.SETTINGS_FIG_DPI, 300))

        plt.close()
