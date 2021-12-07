class DataFittingEnum:
    FILTERED_DATA = "filtered_data"
    CLUSTERED_DATA = "clustered_data"
    FILTERED_CLUSTERED_DATA = "filtered_clustered_data"


class FingerprintEnum:
    AGGREGATED_FINGERPRINT = "aggregated_fingerprint"
    STANDARD_FINGERPRINT = "standard_fingerprint"
    MORGAN_FINGERPRINT = "morgan_fingerprint"
    MACCS_FINGERPRINT = "maccs_fingerprint"

    STANDARD = "STANDARD"
    MORGAN = "MORGAN"
    MACCS = "MACCS"


class GeneratePlotsEnum:
    HEXAGONAL_PLOT = "hexagonal_plot"
    HISTOGRAM_PLOT = "histogram_plot"
    SCATTER_BOXPLOT_PLOT = "scatter_boxplot_plot"
    SCATTER_INTERACTIVE_PLOT = "scatter_interactive_plot"
    SCATTER_STATIC_PLOT = "scatter_static_plot"
    TRISURF_INTERACTIVE_PLOT = "trisurf_interactive_plot"
    TRISURF_STATIC_PLOT = "trisurf_static_plot"


class JsonEnum:
    CHEMDATA_NAME = "json_execution"
    CHEMCHARTS = "chemcharts"
    EXECUTION = "execution"
    TASK = "task"
    INPUT = "input"
    INPUT_TYPE = "input_type"

    COLUMNS = "columns"
    SMILES_COLUMN = "smiles_column"
    SCORES_COLUMN = "scores_column"
    EPOCHS_COLUMN = "epochs_column"

    TYPE = "type"

    PARAMETERS = "parameters"
    USEFEATURES = "useFeatures"
    RANGE_DIM1 = "range_dim1"
    RANGE_DIM2 = "range_dim2"
    K = "k"
    NUM_BINS = "num_bins"

    SETTINGS = "settings"
    PATH = "path"
    VIEW = "view"


class JsonStepsEnum:
    DATA_LOADING = "data_loading"
    GENERATE_FINGERPRINTS = "generate_fingerprints"
    DIMENSIONAL_REDUCTION = "dimensional_reduction"
    FILTERING_DATA = "filtering_data"
    CLUSTERING_DATA = "clustering_data"
    BINNING_SCORES = "binning_scores"
    WRITE_OUT = "write_out"
    GENERATE_PLOT = "generate_plot"
    GENERATE_MOVIE = "generate_movie"


class PlottingEnum:
    PARAMETERS_XLIM = "xlim"
    PARAMETERS_YLIM = "ylim"
    PARAMETERS_SCORELIM = "scorelim"
    PARAMETERS_TITLE = "title"
    PARAMETERS_TOTAL_NUMBER_OBSERVATIONS = "total_number_observations"

    SETTINGS_VIEW = "view"
    SETTINGS_PATH = "path"


class PlotLabellingEnum:
    UMAP_1 = "UMAP_1"
    UMAP_2 = "UMAP_2"
    SCORES = "Scores"


class ReinventEnum:
    SMILES = "SMILES"
    TOTAL_SCORE = "total_score"
    EPOCHS_COLUMN = "Step"


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


class TestPlotMovieEnum:
    MOVIE_UNITTEST = "movie_unittest.mp4"
    PLOT_UNITTEST = "plot_unittest.png"


class TestNameEnum:
    TEST_FINGERPRINT_CONTAINER = "test_fingerprint"





