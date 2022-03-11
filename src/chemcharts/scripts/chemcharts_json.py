#!/usr/bin/env python
#  coding=utf-8

import argparse
import os.path
import sys
import dill
import json

from chemcharts.core.container.chemdata import ChemData
from chemcharts.core.container.fingerprint import *

from chemcharts.core.functions.binning import Binning
from chemcharts.core.functions.dimensional_reduction import DimensionalReduction
from chemcharts.core.functions.clustering import Clustering
from chemcharts.core.functions.filtering import Filtering

from chemcharts.core.plots.base_plot import BasePlot
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
from chemcharts.core.utils.enums import FingerprintEnum
from chemcharts.core.utils.enums import JsonStepsEnum
from chemcharts.core.utils.enums import JsonEnum
from chemcharts.core.utils.enums import ReinventEnum
_GPE = GeneratePlotsEnum
_DFE = DataFittingEnum
_FE = FingerprintEnum
_JSE = JsonStepsEnum
_JE = JsonEnum
_ME = MovieEnum
_RE = ReinventEnum


def initialize_plot(plot_type: str) -> BasePlot:
    if plot_type == _GPE.CONTOUR_PLOT:
        plot_instance = ContourPlot()
    elif plot_type == _GPE.HEXAGONAL_PLOT:
        plot_instance = HexagonalPlot()
    elif plot_type == _GPE.HISTOGRAM_PLOT:
        plot_instance = HistogramPlot()
    elif plot_type == _GPE.SCATTER_BOXPLOT_PLOT:
        plot_instance = ScatterBoxplotPlot()
    elif plot_type == _GPE.SCATTER_INTERACTIVE_PLOT:
        plot_instance = ScatterInteractivePlot()
    elif plot_type == _GPE.SCATTER_STATIC_PLOT:
        plot_instance = ScatterStaticPlot()
    elif plot_type == _GPE.TRISURF_INTERACTIVE_PLOT:
        plot_instance = TrisurfInteractivePlot()
    elif plot_type == _GPE.TRISURF_STATIC_PLOT:
        plot_instance = TrisurfStaticPlot()
    else:
        raise ValueError("Expected keyword (contour_plot/ scatter_static_plot/ scatter_boxplot_plot/ "
                         "scatter_interactive_plot/ histogram_plot/ trisurf_static_plot/ "
                         "trisurf_interactive_plot/ hexagonal_plot) but none was given! "
                         "Not supported: "
                         f"{plot_type}")
    return plot_instance


def main():
    parser = argparse.ArgumentParser(description="implements chemcharts entry points")
    parser.add_argument("-conf", type=str, required=True, help="Path to JSON configuration file.")
    args, args_unk = parser.parse_known_args()

    # load the JSON as dictionary
    with open(args.conf, 'r') as conf_file:
        conf = json.load(conf_file)

    # execute the tasks
    chemdata_list = []
    tasks = conf[_JE.CHEMCHARTS][_JE.EXECUTION]
    for task in tasks:
        if task[_JE.TASK] == _JSE.DATA_LOADING:
            input_elements = task[_JE.INPUT]
            if not isinstance(input_elements, list):
                input_elements = [input_elements]
            if task[_JE.INPUT_TYPE].upper() == "CSV":
                # get column names
                smiles_column = task[_JE.COLUMNS][_JE.SMILES_COLUMN]
                values_columns = task[_JE.COLUMNS].get(_JE.VALUES_COLUMNS, [_RE.TOTAL_SCORE])
                epochs_column = task[_JE.COLUMNS].get(_JE.EPOCHS_COLUMN, _RE.EPOCHS_COLUMN)
                groups_column = task[_JE.COLUMNS].get(_JE.GROUPS_COLUMN, _RE.GROUPS_COLUMN)

                for inp in input_elements:
                    smiles, values_df, epochs, groups = load_smiles(inp,
                                                                    smiles_column=smiles_column,
                                                                    values_columns=values_columns,
                                                                    epochs_column=epochs_column,
                                                                    groups_column=groups_column)
                    next_chemdata = ChemData(name=os.path.basename(inp))
                    next_chemdata.set_values(values_df)
                    next_chemdata.set_smiles(smiles)
                    next_chemdata.set_epochs(epochs)
                    next_chemdata.set_groups(groups)
                    chemdata_list.append(next_chemdata)
            elif task[_JE.INPUT_TYPE].upper() == "PKL":
                with open(task[_JE.INPUT][0], "rb") as dill_file:
                    chemdata_list = dill.load(dill_file)
            else:
                raise ValueError(f"Input type {task[_JE.INPUT_TYPE]} not supported.")

        elif task[_JE.TASK] == _JSE.GENERATE_FINGERPRINTS:
            fp_type = task[_JE.TYPE].upper()
            for chemdata in chemdata_list:
                fps_generator = FingerprintGenerator(chemdata.get_smiles())
                if fp_type == _FE.MACCS:
                    fps = fps_generator.generate_fingerprints_maccs()
                elif fp_type == _FE.MORGAN:
                    fps = fps_generator.generate_fingerprints_morgan()
                elif fp_type == _FE.STANDARD:
                    fps = fps_generator.generate_fingerprints()
                else:
                    raise ValueError(f"Fingerprint type {fp_type} not supported.")
                chemdata.set_fingerprints(fps)

        elif task[_JE.TASK] == _JSE.DIMENSIONAL_REDUCTION:
            dimensional_reduction = DimensionalReduction()
            chemdata_list = dimensional_reduction.calculate(chemdata_list=chemdata_list)

        elif task[_JE.TASK] == _JSE.FILTERING_DATA:
            filtering = Filtering()
            for chemdata in chemdata_list:
                chemdata = filtering.filter_range(chemdata=chemdata,
                                                  range_dim1=task[_JE.PARAMETERS][_JE.RANGE_DIM1],
                                                  range_dim2=task[_JE.PARAMETERS][_JE.RANGE_DIM2])

        elif task[_JE.TASK] == _JSE.CLUSTERING_DATA:
            clustering = Clustering()
            for chemdata in chemdata_list:
                chemdata = clustering.clustering(chemdata=chemdata, k=task[_JE.PARAMETERS][_JE.K])

        elif task[_JE.TASK] == _JSE.BINNING_VALUE:
            binning = Binning()
            for chemdata in chemdata_list:
                chemdata = binning.binning(chemdata=chemdata, num_bins=task[_JE.PARAMETERS][_JE.NUM_BINS])

        elif task[_JE.TASK] == _JSE.WRITE_OUT:
            with open(task[_JE.PATH], "wb") as dill_file:
                dill.dump(chemdata_list, dill_file)

        elif task[_JE.TASK] == _JSE.GENERATE_PLOT:
            plot_type = task[_JE.TYPE].lower()
            plot_instance = initialize_plot(plot_type)
            plot_instance.plot(chemdata_list=chemdata_list,
                               parameters=task[_JE.PARAMETERS],
                               settings=task[_JE.SETTINGS])

        elif task[_JE.TASK] == _JSE.GENERATE_MOVIE:
            plot_type = task[_JE.TYPE].lower()
            plot_instance = initialize_plot(plot_type)
            plot_instance.generate_movie(chemdata_list=chemdata_list,
                                         parameters=task.get(_JE.PARAMETERS, {}),
                                         settings=task.get(_JE.SETTINGS, {}))
        else:
            raise ValueError(f"Task definition {task[_JE.TASK]} not supported.")
        print(f"Task {task[_JE.TASK]} completed.")


if __name__ == "__main__":
    main()

    sys.exit(0)
