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
from chemcharts.core.plots import BasePlot

from chemcharts.core.plots.hexag_plot import HexagonalPlot
from chemcharts.core.plots.histogram_plot import HistogramPlot
from chemcharts.core.plots.scatter_boxplot_plot import ScatterBoxplotPlot
from chemcharts.core.plots.scatter_interactive import ScatterInteractivePlot
from chemcharts.core.plots.scatter_static_plot import ScatterStaticPlot
from chemcharts.core.plots.trisurf_interactive_plot import TrisurfInteractivePlot
from chemcharts.core.plots.trisurf_static_plot import TrisurfStaticPlot

from chemcharts.core.functions.io_functions import load_smiles


def initialize_plot(plot_type: str) -> BasePlot:
    if plot_type == "HEXAGONAL_PLOT":
        plot_instance = HexagonalPlot()
    elif plot_type == "HISTOGRAM_PLOT":
        plot_instance = HistogramPlot()
    elif plot_type == "SCATTER_BOXPLOT_PLOT":
        plot_instance = ScatterBoxplotPlot()
    elif plot_type == "SCATTER_INTERACTIVE_PLOT":
        plot_instance = ScatterInteractivePlot()
    elif plot_type == "SCATTER_STATIC_PLOTt":
        plot_instance = ScatterStaticPlot()
    elif plot_type == "TRISURF_INTERACTIVE_PLOT":
        plot_instance = TrisurfInteractivePlot()
    elif plot_type == "TRISURF_STATIC_PLOT":
        plot_instance = TrisurfStaticPlot()
    else:
        raise ValueError("Expected keyword (scatter_static_plot/ scatter_boxplot_plot/ "
                         "scatter_interactive_plot/ histogram_plot/ trisurf_static_plot/ "
                         "trisurf_interactive_plot/ hexagonal_plot) but none was given! "
                         "Not supported: "
                         f"{plot_type}")
    return plot_instance


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
            dimensional_reduction = DimensionalReduction()
            data = dimensional_reduction.calculate(chemdata=data)

        elif task["task"] == "filtering_data":
            filtering = Filtering()
            data = filtering.filter_range(chemdata=data,
                                          range_dim1=task["parameters"]["range_dim1"],
                                          range_dim2=task["parameters"]["range_dim2"])

        elif task["task"] == "clustering_data":
            clustering = Clustering()
            data = clustering.clustering(chemdata=data, k=task["parameters"]["k"])

        elif task["task"] == "binning_scores":
            binning = Binning()
            data = binning.binning(chemdata=data, num_bins=task["parameters"]["num_bins"])

        elif task["task"] == "write_out":
            with open(task["path"], "wb") as dill_file:
                dill.dump(data, dill_file)

        elif task["task"] == "generate_plot":
            plot_type = task["type"].upper()
            plot_instance = initialize_plot(plot_type)
            plot_instance.plot(chemdata=data,
                               parameters=task["parameters"],
                               settings=task["settings"])

        elif task["task"] == "make_movie":
            plot_type = task["type"].upper()
            plot_instance = initialize_plot(plot_type)
            plot_instance.make_movie(data, task["settings"]["path"])
        else:
            raise ValueError(f"Task definition {task['task']} not supported.")
        print(f"Task {task['task']} completed.")

        # TODO
        # new bee tasks?
        # tanimoto similarity
        # make movie
        # view plot (only when one plot

    sys.exit(0)
