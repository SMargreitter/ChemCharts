import unittest
import os
import numpy as np

from chemcharts.core.container.chemdata import ChemData

from chemcharts.core.container.smiles import Smiles
from chemcharts.core.container.embedding import Embedding
from chemcharts.core.plots.trisurf_plot import TrisurfPlot


class TestTrisurfPlot(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        test_chemdata = ChemData(Smiles([""]), name="test_chemdata")
        embedding = Embedding(np.array([[1, 2],
                                        [2, 2],
                                        [4, 2],
                                        [2, 3],
                                        [2.6, 5],
                                        [11.2, 2],
                                        [5, 1.2],
                                        [4, 5],
                                        [8, 9],
                                        [1, 1],
                                        [15, 1],
                                        [5, 2],
                                        [6, 4],
                                        [6, 1],
                                        [4, 18],
                                        [3, 1],
                                        [1, 9],
                                        [6, 4],
                                        [3, 4],
                                        [7, 8]]))
        scores = [1, 3, 4, 5, 2, 1, 6, 3, 5, 0, 2, 1, 3, 4, 1, 2, 8, 6, 1, 1]

        test_chemdata.set_embedding(embedding)
        test_chemdata.set_scores(scores)
        cls.test_chemdata = test_chemdata

    def setUp(self) -> None:
        pass

    def test_trisurf_plot(self):
        test_plot = TrisurfPlot()
        test_plot.plot(self.test_chemdata, "../plot_unitest.png")
        file_size = os.path.getsize("../plot_unitest.png")
        self.assertTrue(85000 <= file_size <= 90000)
