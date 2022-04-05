from typing import List

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from seaborn import blend_palette
from seaborn.distributions import _freedman_diaconis_bins

from chemcharts.core.container.chemdata import ChemData
from chemcharts.core.plots.base_plot import BasePlot

from chemcharts.core.utils.enums import PlottingEnum
from chemcharts.core.utils.print_dataframe import print_dataframe

_PE = PlottingEnum


def _generate_stats(arrays: List[np.array], names: List[str]) -> pd.DataFrame:
    df = None
    if len(arrays) > 1:
        df = pd.DataFrame({
            "comparison": [None for _ in range(len(arrays))],
            "cosine": [np.NaN for _ in range(len(arrays))]})
        for idx in range(len(arrays)):
            for idy in range(idx + 1, len(arrays)):
                df.at[idx+idy-1, "comparison"] = '_'.join([names[idx], names[idy]])
                df.at[idx+idy-1, "cosine"] = cosine_similarity([arrays[idx]], [arrays[idy]])
    return df


class HexagonalPlot(BasePlot):
    def __init__(self):
        super().__init__()

    @staticmethod
    def _hex_lines(a=None, i=None, off=None):
        if off is None:
            off = [0, 0]
        if a is None:
            a = 2 / np.sqrt(3) * i
        if i is None:
            i = np.sqrt(3) / 2 * a

        h = a / 2

        xy = np.array([[[0, a], [i, h]],
                       [[i, h], [i, -h]],
                       [[i, -h], [0, -a]],
                       [[-i, -h], [0, -a]],  # flipped
                       [[-i, h], [-i, -h]],  # flipped
                       [[0, a], [-i, h]]  # flipped
                       ])
        return xy + off

    def _get_lines(self, hb_current) -> np.ndarray:
        # get hexagon centers that should be highlighted
        verts = hb_current.get_offsets()
        cnts = hb_current.get_array()
        highl = verts[cnts > 0 * cnts.max()]

        # create hexagon lines
        a = ((verts[0, 1] - verts[1, 1]) / 3).round(6)
        i = ((verts[1:, 0] - verts[:-1, 0]) / 2).round(6)
        i = i[i > 0][0]
        lines = np.concatenate([self._hex_lines(a, i, off) for off in highl])
        return lines

    @staticmethod
    def _set_gridsize(total_chemdata: ChemData, gridsize):
        if gridsize is None:
            x_bins = int(min(_freedman_diaconis_bins(total_chemdata.get_embedding().np_array[:, 0]), 50))
            y_bins = int(min(_freedman_diaconis_bins(total_chemdata.get_embedding().np_array[:, 1]), 50))
            gridsize = int(np.mean([x_bins, y_bins]))
        return gridsize

    @staticmethod
    def _generate_jointplot(chemdata_list_idx, xlim, ylim, gridsize, vmin, vmax, cmap, color, extent):
        # if cmap is None, initialize the seaborn default over the matplotlib one
        if cmap is None:
            import matplotlib as mpl
            import seaborn.utils as utils_sb
            color_rgb = mpl.colors.colorConverter.to_rgb(color)
            colors = [utils_sb.set_hls_values(color_rgb, l=l)  # noqa
                      for l in np.linspace(1, 0, 12)]
            cmap = blend_palette(colors, as_cmap=True)
        x = sns.jointplot(x=chemdata_list_idx.get_embedding().np_array[:, 0],
                      y=chemdata_list_idx.get_embedding().np_array[:, 1],
                      xlim=xlim,
                      ylim=ylim,
                      joint_kws={"gridsize": gridsize,
                                 "vmin": vmin,
                                 "vmax": vmax,
                                 "lw": 1,
                                 "cmap": cmap},
                      kind="hex",
                      color=color,
                      extent=extent
                      )

    def plot(self, chemdata_list: List[ChemData], parameters: dict, settings: dict):
        # base class call
        super(HexagonalPlot, self).plot(chemdata_list, parameters, settings)

        # chemdata
        current_chemdata = parameters.get(_PE.PARAMETERS_CURRENT_CHEMDATA, None)
        total_chemdata = parameters.get(_PE.PARAMETERS_TOTAL_CHEMDATA, chemdata_list[0])

        # color palette/cmap
        cmap, color = self._coloring(parameters=parameters)

        # lim setting
        xlim, ylim, valuelim = self._get_lims(chemdata_list=chemdata_list,
                                              parameters=parameters)

        # final path setting
        final_path = settings.get(_PE.SETTINGS_PATH, None)
        self._prepare_folder(path=final_path)

        extent = (xlim[0], xlim[1], ylim[0], ylim[1]) if xlim is not None else None

        # generate fixed gridsize for all following plots to make them equally spaced
        gridsize_input = parameters.get(_PE.PARAMETERS_GRIDSIZE, None)
        gridsize = self._set_gridsize(total_chemdata, gridsize_input)

        # temp path setting
        temp_folder_path, temp_plots_path_list = self._generate_temp_paths(number_paths=len(chemdata_list))

        # loop over ChemData objects and generate plots
        list_occup_arrays = []
        for idx in range(len(chemdata_list)):
            # if current contours are to be plotted we need to generate the appropriate counts (for hexbin
            # identification) here, in order to not override the plotting settings later
            if current_chemdata is not None:
                hb_current = plt.hexbin(x=current_chemdata.get_embedding().np_array[:, 0],
                                        y=current_chemdata.get_embedding().np_array[:, 1],
                                        gridsize=gridsize,
                                        extent=extent)

            # TODO: clean this ugly hack that obtains the array
            list_occup_arrays.append(plt.hexbin(x=chemdata_list[idx].get_embedding().np_array[:, 0],
                                                y=chemdata_list[idx].get_embedding().np_array[:, 1],
                                                gridsize=gridsize,
                                                extent=extent).get_array())

            # generate the counts for the actual plotting
            hb = plt.hexbin(x=total_chemdata.get_embedding().np_array[:, 0],
                            y=total_chemdata.get_embedding().np_array[:, 1],
                            gridsize=gridsize,
                            extent=extent)

            # inspired by 2nd solution from here:
            # https://stackoverflow.com/questions/65469173/matplotlib-add-border-around-group-of-bins-with-most-frequent-values-in-hexbin

            # vmin and vmax
            vmin = 0
            vmax = None
            if parameters.get(_PE.PARMETERS_CROSS_OBJECT_NORMALIZE, True):
                vmax = hb.get_array().max()

            # generates jointplot with hexbin background colors
            self._generate_jointplot(chemdata_list_idx=chemdata_list[idx],
                                     xlim=xlim,
                                     ylim=ylim,
                                     gridsize=gridsize,
                                     vmin=vmin,
                                     vmax=vmax,
                                     cmap=cmap,
                                     color=color,
                                     extent=extent)

            # if selected generate contours for current hexbins
            if current_chemdata is not None:
                lines = self._get_lines(hb_current)

                # select contour lines and draw
                uls, c = np.unique(lines.round(4), axis=0, return_counts=True)
                for l in uls[c == 1]:
                    data = l.transpose()
                    sns.lineplot(x=data[0], y=data[1], lw=2, scalex=False, scaley=False, color="black")

            plt.gcf().set_size_inches(settings.get(_PE.SETTINGS_FIG_SIZE, (8, 8)))
            plt.subplots_adjust(top=parameters.get(_PE.PARAMETERS_PLOT_ADJUST_TOP, 0.9))

            name = f"Dataset_{idx}" if chemdata_list[idx].get_name() == "" else chemdata_list[idx].get_name()
            plt.suptitle(name,
                         fontsize=parameters.get(_PE.PARAMETERS_PLOT_TITLE_FONTSIZE, 14))

            plt.savefig(temp_plots_path_list[idx],
                        format=settings.get(_PE.SETTINGS_FIG_FORMAT, 'png'),
                        dpi=settings.get(_PE.SETTINGS_FIG_DPI, _PE.SETTINGS_FIG_DPI_DEFAULT))

            plt.close("all")

        df_stats = _generate_stats(list_occup_arrays, [c.get_name() for c in chemdata_list])
        print_dataframe(df_stats)

        self._merge_multiple_plots(subplot_paths=temp_plots_path_list,
                                   merged_path=final_path,
                                   title=parameters.get(_PE.PARAMETERS_PLOT_TITLE, "Hexagonal ChemCharts Plot"))
        self._clear_temp_dir(path=temp_folder_path)
