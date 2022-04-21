import unittest
import pandas as pd
import statistics

from chemcharts.core.plots.hexag_plot import HexagonalPlot

from chemcharts.core.utils.enums import PlottingEnum, MovieEnum
from chemcharts.core.utils.enums import TestPathsEnum
from chemcharts.core.utils.enums import TestPlotMovieEnum
from chemcharts.core.utils.enums import TestNameEnum

_ME = MovieEnum()
_PE = PlottingEnum()
_TPE = TestPathsEnum()
_TPME = TestPlotMovieEnum
_TNE = TestNameEnum


class TestHexagonalMedianPlot(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        test_df = pd.DataFrame({"UMAP_1": [1, 1.2, 1.1, 1.4, 5, 8],
                                "UMAP_2": [1, 1.5, 1.8, 1.1, 6, 8],
                                "total_score": [0.963307976722717,
                                                0.939590156078339,
                                                0.93560266494751,
                                                0.92920982837677,
                                                0.829911649227142,
                                                0.829833388328552]
                                })

        cls.test_df = test_df

    def setUp(self) -> None:
        pass

    def test_hex_median(self):
        test_plot = HexagonalPlot()
        hb = test_plot._hex_median(x=self.test_df["UMAP_1"],
                                   y=self.test_df["UMAP_2"],
                                   gridsize=5,
                                   extent=None,
                                   C=self.test_df["total_score"]
                                   )
        calc_median = statistics.median([0.963307976722717,
                                         0.939590156078339,
                                         0.93560266494751,
                                         0.92920982837677])
        all_median_list = list(hb.get_array())

        self.assertEqual(all_median_list[0], calc_median)
