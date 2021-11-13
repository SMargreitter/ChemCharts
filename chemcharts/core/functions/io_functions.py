from typing import Tuple

import pandas as pd
from chemcharts.core.container.smiles import Smiles


def load_smiles(path: str) -> Tuple[Smiles, list]:
    loaded_data = pd.read_csv(path)
    smiles = Smiles(list(loaded_data["SMILES"]))
    scores = list(loaded_data["total_score"])
    return smiles, scores
