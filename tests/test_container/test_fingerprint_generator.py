import unittest

from chemcharts.core.container.fingerprint import *
from chemcharts.core.container.smiles import Smiles


class TestFingerprintGenerator(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.smiles = Smiles(["COc1ccc(-c2c(-c3ccc(S(N)(=O)=O)cc3)[nH]c3ccccc23)cc1",
                             "COc1ccc(-c2c(-c3ccc(S(N)(=O)=O)cc3)oc3ccccc23)cc1F",
                             "Cc1cc(C)c(S(=O)(=O)N2CCN(C(C)c3nc(C(C)(C)C)no3)CC2)c(C)c1"])

    def setUp(self) -> None:
        pass

    def test_standard(self):
        fp_generator = FingerprintGenerator(self.smiles)
        standard_fp_container = fp_generator.generate_fingerprints()
        self.assertListEqual([1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
                             list(standard_fp_container.fingerprint_list[0])[:20])

    def test_morgan(self):
        fp_generator = FingerprintGenerator(self.smiles)

        # testing with useFeatures False
        morgan_fp_container = fp_generator.generate_fingerprints_morgan(False)
        self.assertListEqual([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             list(morgan_fp_container.fingerprint_list[0])[:20])

        # testing with useFeatures True
        morgan_fp_container = fp_generator.generate_fingerprints_morgan(True)
        self.assertListEqual([1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             list(morgan_fp_container.fingerprint_list[0])[:20])

    def test_maccs(self):
        fp_generator = FingerprintGenerator(self.smiles)
        maccs_fp_container = fp_generator.generate_fingerprints_maccs()
        self.assertListEqual([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             list(maccs_fp_container.fingerprint_list[0])[:20])
