import unittest

from chemcharts.core.container.chemdata import ChemData

from chemcharts.core.container.fingerprint import FingerprintContainer
from chemcharts.core.container.smiles import Smiles
from chemcharts.core.functions.dimensional_reduction import DimensionalReduction


class TestDimensionalReduction(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        test_chemdata = ChemData(Smiles(["COc1ccc(-c2c(-c3ccc(S(N)(=O)=O)cc3)[nH]c3ccccc23)cc1",
                                         "COc1ccc(-c2c(-c3ccc(S(N)(=O)=O)cc3)oc3ccccc23)cc1F",
                                         "Cc1cc(C)c(S(=O)(=O)N2CCN(C(C)c3nc(C(C)(C)C)no3)CC2)c(C)c1",
                                         "CN(C)CCN1CCN(c2nnc3ccc(NCc4cc(CNCCNCCN)cc5ccccc45)cn23)CC1",
                                         "CN(C)CCNCc1ccc(C=CCN(CCNCCCN)CCNCCN2C(=O)c3cccc(N)c3C2=O)cc1",
                                         "CCc1nc(-c2cc(CN(CCN)CCN)c(O)c(NCCN(CC)CC)n2)c(CCNCCc2ccc(O)c3c(=O)cc(C)[nH]c23)[nH]1",
                                         "Cn1c(NCc2cc(CNCCNCCNCCN)cc3[nH]c4ccccc4c23)nc2cc(CNc3ccccc3C(N)=O)ccc21",
                                         "N=C(N)c1cc(CN)cc(N=Cc2ccc(-c3ccc(C(N)=NCCN)[nH]3)cc2)c1",
                                         "NCCNCCNCc1ccc2cc(NCCCNCc3ccnc4ccccc34)cc(CNCCNCCNCc3cccc(O)c3)c2c1",
                                         "CNC(=O)c1cccc(Nc2cc(Nc3nccc(-c4cn[nH]c4-c4ccc(CNCCCNCCN)cc4)n3)ccn2)c1",
                                         "NCCCNCCCNCCNCc1ccc(NCCCCNCCNc2ccnc3ccc(C(F)(F)F)cc23)c2cc(N)cc(CCN=C(N)N)c12",
                                         "CCN(CC)CCNCc1cnn(Cc2ccc(CN)cc2)c1CN(CCNC)Cc1ccc(-c2ccc(C(F)(F)F)cc2)cc1C",
                                         "Cc1ccc(C(C)C)c(O)c1C(=O)N=C(CN)NCc1cc(CN)cc(CNC=Nc2ccc(C3=NCCN3)cc2)c1",
                                         "CN(CCN)Cc1ccc(C(=O)NCCNCC(O)COc2ccc(CCNCC(CN)CCCCN)cc2)cc1",
                                         "CNCCCNCc1cc(-c2ccc(CNCCc3cnc[nH]3)cc2)cc(-c2cccc(C(=N)N)c2)c1CN",
                                         "CC(C)(C)c1cc(CNCc2ccc(C(N)=O)c(CNC(=O)CN(CCN)CCCN)c2)cc(C(=O)NN=Cc2cc(CN)ccc2O)c1",
                                         "CN(C)Cc1ccc(CNCCNCc2c(F)c(CN)c(O)c(CNCCNCC(N)CS)c2CNC=N)cc1",
                                         "CN(C)c1cc[n+](Cc2cccc(C[n+]3ccc4c(S(=O)(=O)NCCCNCCCN)cccc4c3)c2)c2ccccc12",
                                         "COc1ccc(-c2c(CNCc3cc(C(F)(F)F)cc(C(F)(F)F)c3)n[nH]c(=O)c2C=Cc2cccc(C(=N)N)c2)cc1CN1CCCCCCC1",
                                         "Cc1ccc2c(c1)c(CNCCNCCNCCN)cc1c3cc(C(=N)N)ccc3cc(CNCCCNCCCNCCCNCCN)c21",
                                         "N#CN=C(N)NCc1ccc(CNc2ccc3ccnc(N)c3c2)c(CNc2cc(CNCCNCCN)ccc2C(N)=O)c1",
                                         "COc1ccc(CCN(Cc2ccc(C(=N)N)cc2)Cc2ccc(C(=N)N)cc2F)c(Br)c1CNCCN",
                                         "Cc1cc(C=Nc2ccc(N=Cc3ccc4ccccc4c3)cc2)c(O)c(CNCCNCCNCCN)c1",
                                         "NCCNCCN(CCNCc1cc2cc(O)ccc2c2cc(N)ccc12)CCNc1c2c(nc3ccccc13)CCCC2",
                                         "CN(C)C1CCN(c2cccc(CNCc3ccc4cn(Cc5ccc(C(=O)NN=Cc6ccc(CN7CCN(Cc8ccccc8)CC7)cc6)cc5)nc4c3)c2)CC1",
                                         "CS(=O)(=O)NCc1ccc(CN2CCN(CC(CSc3ccc([N+](=O)[O-])cc3C#N)n3cnc4ccc(CNCCNCCN)cc4c3=O)CC2)cc1",
                                         "NCCNCCNCCn1ccc2ccc(C(NCCc3sc(N)nc3C(=O)NN)c3cccc(CN)c3)cc21",
                                         "[N-]=[N+]=NCc1cc(CN)c(O)c(CNC(CCN)Cc2cccc(CN)c2)c1CN1CCN(Cc2cccc(CN)c2)CC1",
                                         "NC(N)=NCCCC(CNCCc1c[nH]cn1)NC(=O)C(Cc1ccc(-c2cccc(CN3CCCNCC3)c2)cc1)NCC(=O)NCc1ccc2ccccc2c1",
                                         "CC(C)c1ccc2ccc(C=CC(CCNCCNCCN)=NNc3nc(-c4cc(C(F)(F)F)cc(C(F)(F)F)c4)cs3)c(c1)c2"]),
                                 name="test_chemdata"
                                 )
        test_fingerprint = FingerprintContainer("test_fingerprint",
                                                [[1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
                                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                 [1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                 [1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0],
                                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
                                                 [1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                 [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
                                                 [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                 [1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                 [1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0],
                                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
                                                 [1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                                                 [1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1],
                                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                                                 [1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                                                 [1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0],
                                                 [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                 [1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                                                 [1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
                                                 [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                                 [1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
                                                 [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                                                 [0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                 [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
                                                 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                 [0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                 [1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
                                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
                                                 [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                                 ])
        test_chemdata.set_fingerprints(test_fingerprint)
        cls.test_chemdata = test_chemdata
        cls.test_chemdata_list = [test_chemdata]

    def setUp(self) -> None:
        pass

    def test_array_list(self):
        test_dim_red = DimensionalReduction()
        test_array_list = test_dim_red._generating_array_list(self.test_chemdata.get_fingerprints())
        self.assertListEqual([1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0], list(test_array_list[0]))

    def test_dimensional_reduction(self):
        test_dim_red = DimensionalReduction()
        test_embedding = test_dim_red._dimensional_reduction(self.test_chemdata.get_fingerprints())
        self.assertListEqual([-3, 11], [int(x) for x in list(test_embedding[0])])

    def test_embedding_added_to_chemdata(self):
        test_dim_red = DimensionalReduction()
        test_calculation = test_dim_red.calculate(self.test_chemdata_list)
        self.assertEqual(30, len(test_calculation[0].get_smiles()))
        self.assertEqual(30, len(test_calculation[0].get_fingerprints()))
        self.assertListEqual([-3, 11], [int(x) for x in list(test_calculation[0].get_embedding()[0])])

