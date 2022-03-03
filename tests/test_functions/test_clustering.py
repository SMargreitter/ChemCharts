import unittest
import numpy as np
import pandas as pd

from chemcharts.core.container.chemdata import ChemData

from chemcharts.core.container.smiles import Smiles
from chemcharts.core.container.embedding import Embedding
from chemcharts.core.functions.clustering import Clustering


class TestClustering(unittest.TestCase):
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
        values = pd.DataFrame([1, 3, 4, 5, 2, 1, 6, 3, 5, 0, 2, 1, 3, 4, 1, 2, 8, 6, 1, 1], columns=["test_value"])

        test_chemdata.set_embedding(embedding)
        test_chemdata.set_values(values)
        cls.test_chemdata = test_chemdata

    def test_clustering(self):
        clustering = Clustering()
        clustered_data = clustering.clustering(self.test_chemdata, 10)
        value_length = len(clustered_data.get_values())
        self.assertListEqual([6, 4], [int(x) for x in list(clustered_data.get_embedding()[0])])
        self.assertEqual(value_length, 10)
