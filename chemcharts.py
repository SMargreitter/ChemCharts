#!/usr/bin/env python
#  coding=utf-8

import argparse
import sys
import dill

from chemcharts.core.container.chemdata import ChemData
from chemcharts.core.container.fingerprint import *

from chemcharts.core.functions.dimensional_reduction import DimensionalReduction
from chemcharts.core.functions.clustering import Clustering
from chemcharts.core.functions.filtering import Filtering

from chemcharts.core.plots.hexag_plot import HexagonalPlot
from chemcharts.core.plots.scatter_static_plot import ScatterStaticPlot
from chemcharts.core.plots.scatter_boxplot_plot import ScatterBoxplotPlot
from chemcharts.core.plots.trisurf_plot import TrisurfPlot
from chemcharts.core.plots.scatter_interactive import ScatterInteractivePlot
from chemcharts.core.plots.scatter_density_plot import ScatterDensityPlot

from chemcharts.core.functions.io_functions import load_smiles


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="implements chemcharts entry points")
    parser.add_argument("-input_data", type=str, required=True, help="Path to input csv file.")
    parser.add_argument("-output_plot", type=str, required=True, help="Path to output plot file.")
    parser.add_argument("-k", type=int, required=False, default=10, help="Number of clusters for KMeans.")
    parser.add_argument("-plot", type=str, required=False, default="hexagonal_plot",
                        help="Choose a plot: "
                             "scatter_static_plot" "|"
                             "scatter_boxplot_plot" "|"
                             "scatter_interactive_plot" "|"
                             "scatter_density_plot" "|"
                             "trisurf_plot" "|" 
                             "hexagonal_plot (default)")

    parser.add_argument("-data", type=str, required=False, default="original_data",
                        help="Choose the data set:"
                             "filtered_data,"
                             "clustered_data,"
                             "filtered_clustered_data,"
                             "original_data (default, no filtering or clustering)")
    parser.add_argument("-save_data", type=str, required=False, default=None,
                        help="Path to output processed ChemData object")

    args, args_unk = parser.parse_known_args()

    # load data
    if args.input_data[-4:] == ".pkl":
        with open(args.input_data, "rb") as dill_file:
            plot_data = dill.load(dill_file)
    else:
        smiles, scores, epoch = load_smiles(args.input_data)

        # initialize Chemdata and add smiles and fps
        ori_data = ChemData(smiles_obj=smiles, scores=scores)
        fps_generator = FingerprintGenerator(ori_data.get_smiles())
        fps = fps_generator.generate_fingerprints_maccs()
        ori_data.set_fingerprints(fps)

        # generate embedding (dimensional reduction)
        dimensional_reduction = DimensionalReduction()
        ori_data = dimensional_reduction.calculate(chemdata=ori_data)

        # filter and cluster data
        filtering = Filtering()
        filtered_data = filtering.filter_range(chemdata=ori_data, range_dim1=(-100, 100), range_dim2=(-100, 100))

        clustering = Clustering()
        clustered_data = clustering.clustering(chemdata=ori_data, k=args.k)

        clustering_filtered_data = Clustering()
        filtered_clustered_data = clustering_filtered_data.clustering(chemdata=filtered_data, k=args.k)

        # TODO: add binning

        # choose whether data is filtered and or clustered
        if args.data == "filtered_data":
            plot_data = filtered_data
        elif args.data == "clustered_data":
            plot_data = clustered_data
        elif args.data == "filtered_clustered_data":
            plot_data = filtered_clustered_data
        else:
            plot_data = ori_data

    if args.save_data is not None:
        with open(args.save_data, "wb") as dill_file:
            dill.dump(plot_data, dill_file)

    # generate plots
    if args.plot == "scatter_interactive_plot":
        scatter_interactive_plot = ScatterInteractivePlot()
        scatter_interactive_plot.plot(plot_data, args.output_plot)
    elif args.plot == "scatter_boxplot_plot":
        scatter_boxplot_plot = ScatterBoxplotPlot()
        scatter_boxplot_plot.plot(plot_data, args.output_plot)
    elif args.plot == "trisurf_plot":
        trisurf_plot = TrisurfPlot()
        trisurf_plot.plot(plot_data, args.output_plot)
    elif args.plot == "scatter_static_plot":
        scatter_static_plot = ScatterStaticPlot()
        scatter_static_plot.plot(plot_data, args.output_plot)
    elif args.plot == "scatter_density_plot":
        scatter_density_plot = ScatterDensityPlot
        scatter_density_plot.plot(plot_data, args.output_plot)
    elif args.plot == "hexagonal_plot":
        hex_plot = HexagonalPlot()
        hex_plot.plot(plot_data, args.output_plot)
    else:
        raise ValueError("Expected keyword (scatter_static_plot/ scatter_boxplot_plot/ scatter_interactive_plot/ "
                         "scatter_density_plot/ trisurf_plot/ hexagonal_plot) but none was given! Not supported: "
                         f"{args.plot}")

    sys.exit(0)


