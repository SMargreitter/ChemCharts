import unittest

import numpy as np
from sklearn.cluster import KMeans

from chemcharts.core.container.chemdata import ChemData

from chemcharts.core.container.smiles import Smiles
from chemcharts.core.container.embedding import Embedding
from chemcharts.core.functions.filtering import Filtering
from chemcharts.core.functions.clustering import Clustering


class TestBinning(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        test_chemdata = ChemData(Smiles([""]), name="test_chemdata")
        scores = [1, 3, 4, 5, 2, 1, 6, 3, 5, 0, 2, 1, 3, 4, 1, 2, 8, 6, 1, 1]

        test_chemdata.set_scores(scores)
        cls.test_chemdata = test_chemdata

    def test_clustering(self):
        clustering = Clustering()
        clustered_data = clustering.clustering(self.test_chemdata, 10)
        score_length = len(clustered_data.get_scores())
        self.assertListEqual([6, 4], [int(x) for x in list(clustered_data.get_embedding()[0])])
        self.assertEqual(score_length, 10)