from typing import Tuple

import pandas as pd
from chemcharts.core.container.smiles import Smiles


def load_smiles(path: str,
                smiles_column: str = "SMILES",
                scores_column: str = "total_score",
                epochs_column: str = "Step") -> Tuple[Smiles, list, list]:
    """
    My numpydoc description of a kind
    of very exhautive numpydoc format docstring.

    Parameters
    ----------
    first : array_like
        the 1st param name `first`
    second :
        the 2nd param
    third : {'value', 'other'}, optional
        the 3rd param, by default 'value'

    Returns
    -------
    string
        a value in a string

    Raises
    ------
    KeyError
        when a key error
    OtherError
        when an other error
    """

    loaded_data = pd.read_csv(path)
    smiles = Smiles(list(loaded_data[smiles_column]))
    scores = list(loaded_data[scores_column])
    epoch = list(loaded_data[epochs_column])
    return smiles, scores, epoch
