import unittest
import os
import numpy as np
import shutil
import pandas as pd

from chemcharts.core.container.chemdata import ChemData
from chemcharts.core.container.embedding import Embedding
from chemcharts.core.container.fingerprint import *
from chemcharts.core.container.smiles import Smiles

from chemcharts.core.plots.trisurf_static_plot import TrisurfStaticPlot

from chemcharts.core.utils.enums import PlottingEnum, MovieEnum
from chemcharts.core.utils.enums import TestPathsEnum
from chemcharts.core.utils.enums import TestPlotMovieEnum
from chemcharts.core.utils.enums import TestNameEnum

_PE = PlottingEnum()
_ME = MovieEnum()
_TPE = TestPathsEnum()
_TPME = TestPlotMovieEnum
_TNE = TestNameEnum


class TestTrisurfStaticPlot(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if os.path.isdir(_TPE.PATH_TRISURF_STATIC_TEST):
            shutil.rmtree(_TPE.PATH_TRISURF_STATIC_TEST)
        os.mkdir(_TPE.PATH_TRISURF_STATIC_TEST)

        if os.path.isdir(_TPE.PATH_TRISURF_STATIC_MOVIE):
            shutil.rmtree(_TPE.PATH_TRISURF_STATIC_MOVIE)
        os.mkdir(_TPE.PATH_TRISURF_STATIC_MOVIE)

        smiles = Smiles(["COc1ccc(-c2c(-c3ccc(S(N)(=O)=O)cc3)[nH]c3ccccc23)cc1",
                         "COc1ccc(-c2c(-c3ccc(S(N)(=O)=O)cc3)oc3ccccc23)cc1F",
                         "Cc1cc(C)c(S(=O)(=O)N2CCN(C(C)c3nc(C(C)(C)C)no3)CC2)c(C)c1",
                         "C1ccc2c(c1)-c1ccc3ccccc3c1C2Cc1nn[nH]n1",
                         "Cc1ccccc1-c1c(C(=O)N=c2cccc[nH]2)cnc2ccccc12",
                         "N=c1[nH]c(=O)c2ncn(Cc3cccc4ccccc34)c2[nH]1",
                         "O=C1c2cccc3c(F)ccc(c23)CN1c1cccnc1",
                         "O=C(N=c1cccc[nH]1)c1cnc2ccccc2c1-c1ccc(Cl)cc1",
                         "O=C(N=c1cccc[nH]1)c1cccc2cccc(-c3ccncn3)c12",
                         "Cc1ccc(=NC(=O)c2cc(-c3c(F)cccc3F)nc3ccccc23)[nH]c1",
                         "Cc1cc[nH]c(=NC(=O)c2cccc3c2-c2ccccc2C3=O)c1",
                         "Cc1cccc(-c2ccc3c(=O)[nH]cc(-c4c[nH]c(=O)[nH]c4=O)c3c2)c1",
                         "O=C1c2cccc3cccc(c23)CN1c1cccc(F)c1",
                         "N=C1Cc(O)cc2c3c(c4ccccc4c2C1=O)C(=N)C(=O)C3=O",
                         "Cc1cc[nH]c(=NC(=O)c2cccc3ccccc23)c1",
                         "Cc1cc(Cl)cc(-c2c(C(=O)N=c3cccc[nH]3)ccc3ccccc23)c1",
                         "C1=C(CN2CCNCC2)c2ccccc2-c2ccccc21",
                         "O=C(N=c1cccc[nH]1)c1cccc2c(C(F)(F)F)nc3ccccc3c12",
                         "Cc1cccc(-c2cc(C(=O)N=c3cc(C)cc(C)[nH]3)c3ccccc3n2)c1",
                         "O=C(N=c1cncc[nH]1)c1cccc2c1-c1ccccc1C2=O",
                         "COc1ccc(NC(=O)c2cccc(-c3cc(N4CCCC4)nc(-c4cccs4)n3)c2)cc1",
                         "C(=Nc1ccc(-c2ccc(N=C(c3ccccc3)c3ccccn3)cc2)cc1)c1ccccc1",
                         "COc1ccc(OC)c(NC(=O)Nc2ccc(-c3cc(OC)c(OC)c(OC)c3)cc2)c1",
                         "COc1ccc(-n2nc3ccc(NC(=O)c4cccc(Cl)c4Cl)cc3n2)cc1"])
        embedding_list = Embedding(np.array([[1, 2],
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
                                             [7, 8],
                                             [1, 3],
                                             [4, 4],
                                             [5, 7],
                                             [6, 2]]))
        fingerprint_list = FingerprintContainer(_TNE.TEST_FINGERPRINT_CONTAINER,
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
                                                 [1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1],
                                                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                                                 [1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
                                                 [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0]])
        values = pd.DataFrame([1, 3, 4, 5, 2, 1, 6, 3, 5, 0, 2, 1, 3, 4, 1, 2, 8, 6, 1, 2, 2, 1, 1, 1], columns=["test_value"])
        epochs = [0, 1, 1, 3, 0, 2, 2, 0, 1, 3, 0, 3, 2, 3, 2, 3, 1, 0, 0, 3, 2, 1, 1, 2]

        test_data_set = ChemData(smiles)
        test_data_set.set_embedding(embedding_list)
        test_data_set.set_fingerprints(fingerprint_list)
        test_data_set.set_values(values)
        test_data_set.set_epochs(epochs)
        cls.test_chemdata = test_data_set

    def setUp(self) -> None:
        pass

    def test_trisurf_static_plot(self):
        test_plot = TrisurfStaticPlot()
        settings = {_PE.SETTINGS_PATH: '/'.join([_TPE.PATH_TRISURF_STATIC_TEST, _TPME.PLOT_UNITTEST])}
        parameters = {_PE.PARAMETERS_XLIM: None,
                      _PE.PARAMETERS_YLIM: None,
                      _PE.PARAMETERS_VALUELIM: [None, None],
                      _PE.PARAMETERS_VALUECOLUMN: "test_value",
                      _PE.PARAMETERS_VALUENAME: "Value"
                      }
        test_plot.plot([self.test_chemdata], parameters, settings)
        file_size = os.path.getsize('/'.join([_TPE.PATH_TRISURF_STATIC_TEST, _TPME.PLOT_UNITTEST]))
        self.assertTrue(250000 <= file_size <= 350000)

    def test_check_movie_size(self):
        test_plot = TrisurfStaticPlot()
        settings = {_ME.SETTINGS_MOVIE_PATH: '/'.join([_TPE.PATH_TRISURF_STATIC_MOVIE, _TPME.MOVIE_UNITTEST])}
        parameters = {_PE.PARAMETERS_VALUECOLUMN: "test_value",
                      _PE.PARAMETERS_VALUENAME: "Value"
                      }
        test_plot.generate_movie([self.test_chemdata], parameters, settings)
        file_size = os.path.getsize('/'.join([_TPE.PATH_TRISURF_STATIC_MOVIE, _TPME.MOVIE_UNITTEST]))
        self.assertTrue(100000 <= file_size <= 200000)
