import unittest

from chemcharts.core.container.smiles import Smiles


class TestSmiles(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.smiles_list = ["COc1ccc(-c2c(-c3ccc(S(N)(=O)=O)cc3)[nH]c3ccccc23)cc1",
                           "COc1ccc(-c2c(-c3ccc(S(N)(=O)=O)cc3)oc3ccccc23)cc1F",
                           "Cc1cc(C)c(S(=O)(=O)N2CCN(C(C)c3nc(C(C)(C)C)no3)CC2)c(C)c1"]

    def setUp(self) -> None:
        pass

    def test_smiles(self):
        test_smiles = Smiles(self.smiles_list)
        self.assertIn("COc1ccc(-c2c(-c3ccc(S(N)(=O)=O)cc3)[nH]c3ccccc23)cc1", test_smiles)

    def test_get_len(self):
        test_smiles = Smiles(self.smiles_list)
        length = len(test_smiles)
        self.assertEqual(length, 3)
