from copy import deepcopy
from rdkit import DataStructs
import numpy as np

from chemcharts.core.container.chemdata import ChemData


class Binning:
    def __init__(self):
        pass

    @staticmethod
    def binning(chemdata: ChemData) -> ChemData:
        chemdata = deepcopy(chemdata)
        np.linspace(start=-2.1, stop=8.0, num=3)
        np.digitize([1.333, 2.33, -1, -2, -1.3, 7.9], bins=[-2.1, 2.95, 8.]) - 1

        return chemdata
