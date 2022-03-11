from chemcharts.core.utils.files_paths import attach_root_path


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
    CONTOUR_PLOT = "contour_plot"
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
    VALUES_COLUMNS = "values_columns"
    EPOCHS_COLUMN = "epochs_column"
    GROUPS_COLUMN = "groups_column"

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
    BOXPLOT = "boxplot"
    GROUP_NAME = "group_name"


class JsonStepsEnum:
    DATA_LOADING = "data_loading"
    GENERATE_FINGERPRINTS = "generate_fingerprints"
    DIMENSIONAL_REDUCTION = "dimensional_reduction"
    FILTERING_DATA = "filtering_data"
    CLUSTERING_DATA = "clustering_data"
    BINNING_VALUE = "binning_values"
    WRITE_OUT = "write_out"
    GENERATE_PLOT = "generate_plot"
    GENERATE_MOVIE = "generate_movie"


class MovieEnum:
    PARAMETERS = "parameters"
    PARAMETERS_USE_CURRENT_EPOCH = "use_current_epoch"

    SETTINGS = "settings"
    SETTINGS_MOVIE_PATH = "movie_path"

    ENDING_GIF = ".gif"
    ENDING_MP4 = ".mp4"


class PlottingEnum:
    PARAMETERS_GRIDSIZE = "gridsize"
    PARAMETERS_BINS = "bins"
    PARMETERS_CROSS_OBJECT_NORMALIZE = "cross_object_normalize"

    PARAMETERS_PLOT_TITLE = "title"
    PARAMETERS_PLOT_TITLE_FONTSIZE = "fontsize"
    PARAMETERS_PLOT_ADJUST_TOP = "top"
    PARAMETERS_PLOT_COLOR = "color"
    PARAMETERS_PLOT_S = "s"                      #3d scatter plot ball size
    PARAMETERS_PLOT_MARKER_SIZE = "marker_size"
    PARAMETERS_BW_ADJUST = "bw_adjust"
    PARAMETERS_SHADE = "shade"
    PARAMETERS_THRESH = "thresh"
    PARAMETERS_MESH_CLOSENESS = "mesh_closeness"

    PARAMETERS_VALUECOLUMN = "value_column"
    PARAMETERS_VALUENAME = "value_name"
    PARAMETERS_VALUELIM = "valuelim"
    PARAMETERS_YLIM = "ylim"
    PARAMETERS_XLIM = "xlim"

    PARAMETERS_VMIN = "vmin"
    PARAMETERS_VMAX = "vmax"

    PARAMETERS_CURRENT_CHEMDATA = "current_chemdata"
    PARAMETERS_TOTAL_CHEMDATA = "total_chemdata"

    PARAMETERS_MODE = "mode"
    PARAMETERS_GROUP_LEGEND_NAME = "group_legend_name"
    PARAMETERS_GROUP_LEGEND_NAME_DEFAULT = "groups"

    SETTINGS_FIG_FORMAT = "format"
    SETTINGS_FIG_DPI = "dpi"
    SETTINGS_FIG_DPI_DEFAULT = 300
    SETTINGS_FIG_SIZE = "figsize"

    SETTINGS_VIEW = "view"
    SETTINGS_PATH = "path"
    SETTINGS_BOXPLOT = "boxplot"


class PlotLabellingEnum:
    UMAP_1 = "UMAP_1"
    UMAP_2 = "UMAP_2"
    VALUES = "Values"
    GROUPS = "Groups"


class ReinventEnum:
    SMILES = "SMILES"
    TOTAL_SCORE = "total_score"
    EPOCHS_COLUMN = "Step"
    GROUPS_COLUMN = "groups"


class TestPathsEnum:
    PATH_HEXAGONAL_TEST = attach_root_path("tests/junk/hexagonal_plot")
    PATH_HEXAGONAL_MOVIE = attach_root_path("tests/junk/hexagonal_movie")

    PATH_CONTOUR_TEST = attach_root_path("tests/junk/contour_plot")
    PATH_CONTOUR_MOVIE = attach_root_path("tests/junk/contour_movie")

    PATH_HISTOGRAM_TEST = attach_root_path("tests/junk/histogram_plot")
    PATH_HISTOGRAM_MOVIE = attach_root_path("tests/junk/histogram_movie")

    PATH_SCATTER_BOXPLOT_TEST = attach_root_path("tests/junk/scatter_boxplot_plot")
    PATH_SCATTER_BOXPLOT_MOVIE = attach_root_path("tests/junk/scatter_boxplot_movie")

    PATH_SCATTER_INTERACTIVE_TEST = attach_root_path("tests/junk/scatter_interactive_plot")
    PATH_SCATTER_INTERACTIVE_MOVIE = attach_root_path("tests/junk/scatter_interactive_movie")

    PATH_SCATTER_STATIC_TEST = attach_root_path("tests/junk/scatter_static_plot")
    PATH_SCATTER_STATIC_MOVIE = attach_root_path("tests/junk/scatter_static_movie")

    PATH_TRISURF_INTERACTIVE_TEST = attach_root_path("tests/junk/trisurf_interactive_plot")

    PATH_TRISURF_STATIC_TEST = attach_root_path("tests/junk/trisurf_static_plot")
    PATH_TRISURF_STATIC_MOVIE = attach_root_path("tests/junk/trisurf_static_movie")


class TestPlotMovieEnum:
    MOVIE_UNITTEST = "movie_unittest.mp4"
    PLOT_UNITTEST = "plot_unittest.png"


class TestNameEnum:
    TEST_FINGERPRINT_CONTAINER = "test_fingerprint"
