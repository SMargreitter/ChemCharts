import unittest

import numpy as np
from sklearn.cluster import KMeans

from chemcharts.core.container.chemdata import ChemData

from chemcharts.core.container.smiles import Smiles
from chemcharts.core.container.embedding import Embedding
from chemcharts.core.container.fingerprint import *
from chemcharts.core.functions.binning import Binning
from chemcharts.core.functions.filtering import Filtering
from chemcharts.core.functions.clustering import Clustering


class TestBinning(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        smiles = Smiles(["COc1ccc(-c2c(-c3ccc(S(N)(=O)=O)cc3)[nH]c3ccccc23)cc1",
                         "COc1ccc(-c2c(-c3ccc(S(N)(=O)=O)cc3)oc3ccccc23)cc1F",
                         "Cc1cc(C)c(S(=O)(=O)N2CCN(C(C)c3nc(C(C)(C)C)no3)CC2)c(C)c1",
                         "C1ccc2c(c1)-c1ccc3ccccc3c1C2Cc1nn[nH]n1",
                         "Cc1ccccc1-c1c(C(=O)N=c2cccc[nH]2)cnc2ccccc12",
                         "N=c1[nH]c(=O)c2ncn(Cc3cccc4ccccc34)c2[nH]1",
                         "O=C1c2cccc3c(F)ccc(c23)CN1c1cccnc1"])
        scores = [1.333, 2.33, -1, 4.3, 7.9, 9.5, 5.1]

        test_data_set = ChemData(smiles)
        test_data_set.set_scores(scores)
        cls.test_chemdata = test_data_set

    def test_binning(self):
        binning = Binning()
        test_binning = binning.binning(self.test_chemdata, 4)
        self.assertListEqual([1.333, 1.333, 1.333, 4.699999999999999, 8.7, 8.7, 4.699999999999999], test_binning.get_scores())

        #self.assertListEqual([6, 4], [int(x) for x in list(clustered_data.get_embedding()[0])])
        #self.assertEqual(score_length, 10)
