class PlottingEnum:
    PARAMETERS_XLIM = "xlim"
    PARAMETERS_YLIM = "ylim"
    PARAMETERS_SCORELIM = "scorelim"
    PARAMETERS_TOTAL_NUMBER_OBSERVATIONS = "total_number_observations"

    SETTINGS_VIEW = "view"
    SETTINGS_PATH = "path"


class GeneratePlotsEnum:
    HEXAGONAL_PLOT = "hexagonal_plot"
    HISTOGRAM_PLOT = "histogram_plot"
    SCATTER_BOXPLOT_PLOT = "scatter_boxplot_plot"
    SCATTER_INTERACTIVE_PLOT = "scatter_interactive_plot"
    SCATTER_STATIC_PLOT = "scatter_static_plot"
    TRISURF_INTERACTIVE_PLOT = "trisurf_interactive_plot"
    TRISURF_STATIC_PLOT = "trisurf_static_plot"


class TestPathsEnum:
    PATH_HEXAGONAL_TEST = "../junk/hexagonal_plot"
    PATH_HEXAGONAL_MOVIE = "../junk/hexagonal_movie"

    PATH_HISTOGRAM_TEST = "../junk/histogram_plot"
    PATH_HISTOGRAM_MOVIE = "../junk/histogram_movie"

    PATH_SCATTER_BOXPLOT_TEST = "../junk/scatter_boxplot_plot"
    PATH_SCATTER_BOXPLOT_MOVIE = "../junk/scatter_boxplot_movie"

    PATH_SCATTER_INTERACTIVE_TEST = "../junk/scatter_interactive_plot"
    PATH_SCATTER_INTERACTIVE_MOVIE = "../junk/scatter_interactive_movie"

    PATH_SCATTER_STATIC_TEST = "../junk/scatter_static_plot"
    PATH_SCATTER_STATIC_MOVIE = "../junk/scatter_static_movie"

    PATH_TRISURF_INTERACTIVE_TEST = "../junk/trisurf_interactive_plot"

    PATH_TRISURF_STATIC_TEST = "../junk/trisurf_static_plot"
    PATH_TRISURF_STATIC_MOVIE = "../junk/trisurf_static_movie"


class DataFittingEnum:
    FILTERED_DATA = "filtered_data"
    CLUSTERED_DATA = "clustered_data"
    FILTERED_CLUSTERED_DATA = "filtered_clustered_data"


class ReinventEnum:
    SMILES = "SMILES"
    TOTAL_SCORE = "total_score"
    EPOCHS_COLUMN = "Step"