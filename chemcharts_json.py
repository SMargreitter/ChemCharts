#!/usr/bin/env python
#  coding=utf-8

import argparse
import sys
import dill
import json

from chemcharts.core.container.chemdata import ChemData
from chemcharts.core.container.fingerprint import *

from chemcharts.core.functions.binning import Binning
from chemcharts.core.functions.dimensional_reduction import DimensionalReduction
from chemcharts.core.functions.clustering import Clustering
from chemcharts.core.functions.filtering import Filtering

from chemcharts.core.plots.hexag_plot import HexagonalPlot
from chemcharts.core.plots.scatter_static_plot import ScatterStaticPlot
from chemcharts.core.plots.scatter_boxplot_plot import ScatterBoxplotPlot
from chemcharts.core.plots.trisurf_plot import TrisurfInteractivePlot
from chemcharts.core.plots.scatter_interactive import ScatterInteractivePlot
from chemcharts.core.plots.scatter_density_plot import HistogramPlot

from chemcharts.core.functions.io_functions import load_smiles


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="implements chemcharts entry points")
    parser.add_argument("-conf", type=str, required=True, help="Path to JSON configuration file.")
    args, args_unk = parser.parse_known_args()

    # load the JSON as dictionary
    with open(args.conf, 'r') as conf_file:
        conf = json.load(conf_file)

    # execute the tasks
    data = ChemData(name="json_execution")
    tasks = conf["chemcharts"]["execution"]
    for task in tasks:
        if task["task"] == "data_loading":
            if task["input_type"].upper() == "CSV":
                # get column names
                smiles_column = task["columns"]["smiles_column"]
                scores_column = task["columns"]["scores_column"]
                epochs_column = task["columns"]["epochs_column"]
                smiles, scores, epochs = load_smiles(task["input"],
                                                     smiles_column=smiles_column,
                                                     scores_column=scores_column,
                                                     epochs_column=epochs_column)
                data.set_scores(scores)
                data.set_smiles(smiles)
                data.set_epochs(epochs)
            elif task["input_type"].upper() == "PKL":
                with open(task["input"], "rb") as dill_file:
                    data = dill.load(dill_file)
            else:
                raise ValueError(f"Input type {task['input_type']} not supported (yet).")
        elif task["task"] == "generate_fingerprints":
            fp_type = task["type"].upper()
            fps_generator = FingerprintGenerator(data.get_smiles())
            if fp_type == "MACCS":
                fps = fps_generator.generate_fingerprints_maccs()
            elif fp_type == "MORGAN":
                fps = fps_generator.generate_fingerprints_morgan()
            elif fp_type == "STANDARD":
                fps = fps_generator.generate_fingerprints()
            else:
                raise ValueError(f"Fingerprint type {fp_type} not supported.")
            data.set_fingerprints(fps)
        elif task["task"] == "dimensional_reduction":
            pass # do dim red
        elif task["task"] == "filtering_data":
            pass # do filtering
        elif task["task"] == "clustering_data":
            pass # do clustering
        elif task["task"] == "binning_scores":
            pass # bin the scores
        elif task["task"] == "write_out":
            pass # writeout chemdata object
        elif task["task"] == "generate_plot":
            pass # generate plot
        elif task["task"] == "make_movie":
            pass # make movie
        else:
            raise ValueError(f"Task definition {task['task']} not supported.")

    """"# load data
    if args.input_data[-4:] == ".pkl":
        with open(args.input_data, "rb") as dill_file:
            plot_data = dill.load(dill_file)
    else:
        smiles, scores, epochs = load_smiles(args.input_data)

        # initialize Chemdata and add smiles and fps
        ori_data = ChemData(smiles_obj=smiles, scores=scores)
        fps_generator = FingerprintGenerator(ori_data.get_smiles())
        fps = fps_generator.generate_fingerprints_maccs()
        ori_data.set_fingerprints(fps)
        ori_data.set_epochs(epochs)

        # generate embedding (dimensional reduction)
        dimensional_reduction = DimensionalReduction()
        ori_data = dimensional_reduction.calculate(chemdata=ori_data)

        # choose whether data is filtered and or clustered
        plot_data = ori_data
        if args.data == "filtered_data" or args.data == "filtered_clustered_data":
            filtering = Filtering()
            plot_data = filtering.filter_range(chemdata=plot_data, range_dim1=(-100, 100), range_dim2=(-100, 100))
        if args.data == "clustered_data" or args.data == "filtered_clustered_data":
            clustering = Clustering()
            plot_data = clustering.clustering(chemdata=plot_data, k=args.k)

        # binning of scores
        if args.binning is not None:
            binning = Binning()
            plot_data = binning.binning(chemdata=plot_data, num_bins=args.binning)

    if args.save_data is not None:
        with open(args.save_data, "wb") as dill_file:
            dill.dump(plot_data, dill_file)

    # generate plots
    if args.plot == "scatter_interactive_plot":
        plot_instance = ScatterInteractivePlot()
    elif args.plot == "scatter_boxplot_plot":
        plot_instance = ScatterBoxplotPlot()
    elif args.plot == "trisurf_plot":
        plot_instance = TrisurfPlot()
    elif args.plot == "scatter_static_plot":
        plot_instance = ScatterStaticPlot()
    elif args.plot == "scatter_density_plot":
        plot_instance = ScatterDensityPlot()
    elif args.plot == "hexagonal_plot":
        plot_instance = HexagonalPlot()
    else:
        raise ValueError("Expected keyword (scatter_static_plot/ scatter_boxplot_plot/ scatter_interactive_plot/ "
                         "scatter_density_plot/ trisurf_plot/ hexagonal_plot) but none was given! Not supported: "
                         f"{args.plot}")

    #make plot
    plot_instance.plot(plot_data, args.output_plot)

    #make movie
    if args.output_movie is not None:
        plot_instance.make_movie(plot_data, args.output_movie)

    sys.exit(0)

    # JSON:
    # - tanimoto similarity
    # - make movie
"""

