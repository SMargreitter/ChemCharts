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

    def test_set_item(self):
        test_smiles = Smiles(self.smiles_list)
        test_smiles.__setitem__("Fc1ccnc(Cc2cccc3c2-c2ccccc2C3)c1", 1)
        self.assertEqual("Fc1ccnc(Cc2cccc3c2-c2ccccc2C3)c1", test_smiles.__getitem__(1))

    def test_add_item(self):
        test_smiles = Smiles(self.smiles_list)
        concatenated_smiles = test_smiles.__add__(Smiles(["Fc1ccnc(Cc2cccc3c2-c2ccccc2C3)c1"]))
        self.assertIn("Fc1ccnc(Cc2cccc3c2-c2ccccc2C3)c1", concatenated_smiles.smiles_list)
