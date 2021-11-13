import unittest
import numpy as np
from rdkit import Chem

from chemcharts.core.container.chemdata import ChemData

from chemcharts.core.container.fingerprint import FingerprintContainer
from chemcharts.core.container.smiles import Smiles
from chemcharts.core.functions.tanimoto_similarity import TanimotoSimilarity


class TestTanimotoSimilarity(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        test_chemdata = ChemData(Smiles([""]), name="test_chemdata")
        test_fingerprint = FingerprintContainer("test_fingerprint",
                                                [Chem.RDKFingerprint(Chem.MolFromSmiles('CCOC')),
                                                 Chem.RDKFingerprint(Chem.MolFromSmiles('CCO')),
                                                 Chem.RDKFingerprint(Chem.MolFromSmiles('COC')),
                                                 Chem.RDKFingerprint(Chem.MolFromSmiles('COCC'))])
        test_chemdata.set_fingerprints(test_fingerprint)
        cls.test_chemdata = test_chemdata

    def setUp(self) -> None:
        pass

    def test_tanimoto_similarity(self):
        test_tan_sim = TanimotoSimilarity()
        tan_sim_chemdata = test_tan_sim.simplify(self.test_chemdata)
        tan_sim = tan_sim_chemdata.get_tanimoto_similarity()
        self.assertListEqual([0.6, 0.4, 1.0], list(tan_sim[0][1:]))
        self.assertListEqual([0.4], list(tan_sim[-2][3:]))
        self.assertEqual(4, len(list(tan_sim[-1])))
