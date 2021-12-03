from typing import Tuple

import pandas as pd
from chemcharts.core.container.smiles import Smiles

from chemcharts.core.utils.enums import ReinventEnum
_RE = ReinventEnum


def load_smiles(path: str,
                smiles_column: str = _RE.SMILES,
                scores_column: str = _RE.TOTAL_SCORE,
                epochs_column: str = _RE.EPOCHS_COLUMN) -> Tuple[Smiles, list, list]:
    """
         The load_smiles function loads data from a file and allocates its data to a SmilesClass object
         and to a score as well as epoch list.

         Parameters
         ----------
         path: str
            path to the file containing the data
         smiles_column: str = "SMILES"
            the file column containing the smiles
         scores_column: str = "total_score"
            the file column containing the total_score
         epochs_column: str = "Step"
            the file column containing the epochs

         Returns
         -------
         ChemData
             returns a Tuple object containing a SmilesClass object as well as score and epoch lists
    """

    loaded_data = pd.read_csv(path)
    smiles = Smiles(list(loaded_data[smiles_column]))
    scores = list(loaded_data[scores_column])
    epoch = list(loaded_data[epochs_column])
    return smiles, scores, epoch
