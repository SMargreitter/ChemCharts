#!/usr/bin/env python
#  coding=utf-8

import argparse
import sys
import dill

from chemcharts.core.container.chemdata import ChemData
from chemcharts.core.container.fingerprint import *

from chemcharts.core.functions.binning import Binning
from chemcharts.core.functions.dimensional_reduction import DimensionalReduction
from chemcharts.core.functions.clustering import Clustering
from chemcharts.core.functions.filtering import Filtering

from chemcharts.core.plots.contour_plot import ContourPlot
from chemcharts.core.plots.hexag_plot import HexagonalPlot
from chemcharts.core.plots.histogram_plot import HistogramPlot
from chemcharts.core.plots.scatter_boxplot_plot import ScatterBoxplotPlot
from chemcharts.core.plots.scatter_interactive import ScatterInteractivePlot
from chemcharts.core.plots.scatter_static_plot import ScatterStaticPlot
from chemcharts.core.plots.trisurf_interactive_plot import TrisurfInteractivePlot
from chemcharts.core.plots.trisurf_static_plot import TrisurfStaticPlot

from chemcharts.core.functions.io_functions import load_smiles

from chemcharts.core.utils.enums import GeneratePlotsEnum, MovieEnum
from chemcharts.core.utils.enums import DataFittingEnum
from chemcharts.core.utils.enums import PlottingEnum
_GPE = GeneratePlotsEnum
_DFE = DataFittingEnum
_PE = PlottingEnum
_ME = MovieEnum


def main():
    parser = argparse.ArgumentParser(description="implements chemcharts entry points")
    parser.add_argument("-input_data", type=str, required=True,
                        help="Path to input csv file (Caution: Here only one input dataset is possible - "
                             "for multiple input data use the Json version)")
    parser.add_argument("-output_plot", type=str, required=True,
                        help="Path to output plot file.")
    parser.add_argument("-output_movie", type=str, required=False, default=None,
                        help="Path to output movie.")
    parser.add_argument("-dataset_name", type=str, required=False, default=None,
                        help="Name your dataset.")
    parser.add_argument("-save_data", type=str, required=False, default=None,
                        help="Path to output processed ChemData object")
    parser.add_argument("-k", type=int, required=False, default=10,
                        help="Number of clusters for KMeans.")
    parser.add_argument("-plot", type=str, required=False, default="hexagonal_plot",
                        help="Choose a plot: "
                             "contour_plot" "|"
                             "scatter_static_plot" "|"
                             "scatter_boxplot_plot" "|"
                             "scatter_interactive_plot" "|"
                             "histogram_plot (no movie function possible)" "|"
                             "trisurf_static_plot" "|"
                             "trisurf_interactive_plot (no movie function possible)" "|"
                             "hexagonal_plot (default)")
    parser.add_argument("-view", type=bool, required=False, default=False,
                        help="Choose view setting of interactive plots with 'True' or 'False'")
    parser.add_argument("-data", type=str, required=False, default="original_data",
                        help="Choose the data set:"
                             "filtered_data,"
                             "clustered_data,"
                             "filtered_clustered_data,"
                             "original_data (default, no filtering or clustering)")
    parser.add_argument("-binning", type=int, required=False, default=None,
                        help="Choose the amount of bins")

    args, args_unk = parser.parse_known_args()

    # load data
    if args.input_data[-4:] == ".pkl":
        with open(args.input_data, "rb") as dill_file:
            plot_data = dill.load(dill_file)
    else:
        smiles, values_df, epochs, groups = load_smiles(args.input_data)

        # initialize chemdata_list with ONE Chemdata object and add smiles and fps
        ori_data = [ChemData(smiles_obj=smiles, name=args.dataset_name)]
        fps_generator = FingerprintGenerator(ori_data[0].get_smiles())
        fps = fps_generator.generate_fingerprints()
        ori_data[0].set_values(values_df)
        ori_data[0].set_fingerprints(fps)
        ori_data[0].set_epochs(epochs)
        ori_data[0].set_groups(groups)

        # generate embedding (dimensional reduction)
        dimensional_reduction = DimensionalReduction()
        ori_data = dimensional_reduction.calculate(chemdata_list=ori_data)

        # choose whether data is filtered and or clustered
        plot_data = ori_data
        if args.data == _DFE.FILTERED_DATA or args.data == _DFE.FILTERED_CLUSTERED_DATA:
            filtering = Filtering()
            plot_data[0] = filtering.filter_range(chemdata=plot_data[0],
                                                  range_dim1=(-100, 100),
                                                  range_dim2=(-100, 100))
        if args.data == _DFE.CLUSTERED_DATA or args.data == _DFE.FILTERED_CLUSTERED_DATA:
            clustering = Clustering()
            plot_data[0] = clustering.clustering(chemdata=plot_data[0], k=args.k)

        # binning of values
        if args.binning is not None:
            binning = Binning()
            plot_data[0] = binning.binning(chemdata=plot_data[0], num_bins=args.binning)

    if args.save_data is not None:
        with open(args.save_data, "wb") as dill_file:
            dill.dump(plot_data, dill_file)

    # generate plots
    if args.plot == _GPE.CONTOUR_PLOT:
        plot_instance = ContourPlot()
    elif args.plot == _GPE.HEXAGONAL_PLOT:
        plot_instance = HexagonalPlot()
    elif args.plot == _GPE.HISTOGRAM_PLOT:
        plot_instance = HistogramPlot()
    elif args.plot == _GPE.SCATTER_BOXPLOT_PLOT:
        plot_instance = ScatterBoxplotPlot()
    elif args.plot == _GPE.SCATTER_INTERACTIVE_PLOT:
        plot_instance = ScatterInteractivePlot()
    elif args.plot == _GPE.SCATTER_STATIC_PLOT:
        plot_instance = ScatterStaticPlot()
    elif args.plot == _GPE.TRISURF_INTERACTIVE_PLOT:
        plot_instance = TrisurfInteractivePlot()
    elif args.plot == _GPE.TRISURF_STATIC_PLOT:
        plot_instance = TrisurfStaticPlot()
    else:
        raise ValueError("Expected keyword (contour_plot/ scatter_static_plot/ scatter_boxplot_plot/ "
                         "scatter_interactive_plot/ histogram_plot/ trisurf_static_plot/ "
                         "trisurf_interactive_plot/ hexagonal_plot) but none was given! Not supported: "
                         f"{args.plot}")

    # make plot
    plot_instance.plot(chemdata_list=plot_data,
                       parameters={_PE.PARAMETERS_XLIM: None,
                                   _PE.PARAMETERS_YLIM: None,
                                   _PE.PARAMETERS_VALUELIM: None,
                                   _PE.PARAMETERS_CURRENT_CHEMDATA: None,
                                   _PE.PARAMETERS_TOTAL_CHEMDATA: plot_data[0],
                                   _PE.PARAMETERS_VALUECOLUMN: "total_scores",
                                   _PE.PARAMETERS_VALUENAME: "Scores"}
    ,
                       settings={_PE.SETTINGS_VIEW: args.view,
                                 _PE.SETTINGS_PATH: args.output_plot,
                                 _PE.SETTINGS_BOXPLOT: True})

    # make movie
    if args.output_movie is not None:
        plot_instance.generate_movie(plot_data, settings={_ME.SETTINGS_MOVIE_PATH: args.output_movie})


if __name__ == "__main__":
    main()

    sys.exit(0)
