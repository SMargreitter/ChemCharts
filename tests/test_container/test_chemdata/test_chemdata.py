import unittest

import numpy as np

from chemcharts.core.container.chemdata import ChemData
from chemcharts.core.container.embedding import Embedding
from chemcharts.core.container.smiles import Smiles


class TestChemData(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.smiles = Smiles(["COc1ccc(-c2c(-c3ccc(S(N)(=O)=O)cc3)[nH]c3ccccc23)cc1",
                             "COc1ccc(-c2c(-c3ccc(S(N)(=O)=O)cc3)oc3ccccc23)cc1F",
                             "Cc1cc(C)c(S(=O)(=O)N2CCN(C(C)c3nc(C(C)(C)C)no3)CC2)c(C)c1"])
        cls.embedding = Embedding(np.array([[1, 2],
                                            [2, 2],
                                            [4, 2],
                                            [2, 3],
                                            [2.6, 5],
                                            [11.2, 2],
                                            [5, 1.2],
                                            [4, 5]]))

    def setUp(self) -> None:
        pass

    def test_set_smile_to_chemdata(self):
        test_data_set = ChemData(self.smiles)
        test_data_set.set_smiles(self.smiles)
        self.assertIsInstance(test_data_set.get_smiles(), Smiles)
        self.assertEqual(test_data_set.get_smiles()[1], "COc1ccc(-c2c(-c3ccc(S(N)(=O)=O)cc3)oc3ccccc23)cc1F")

    def test_set_embedding(self):
        test_data_set = ChemData(self.smiles)
        test_data_set.set_embedding(self.embedding)
        self.assertIsInstance(test_data_set.get_embedding(), Embedding)
        self.assertListEqual([1, 2], [int(x) for x in list(test_data_set.get_embedding()[0])])
