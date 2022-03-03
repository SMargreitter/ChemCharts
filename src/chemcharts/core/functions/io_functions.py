from typing import Tuple

import pandas as pd
from chemcharts.core.container.smiles import Smiles

from chemcharts.core.utils.enums import ReinventEnum
_RE = ReinventEnum


def load_smiles(path: str,
                smiles_column: str = _RE.SMILES,
                values_columns: list = [_RE.TOTAL_SCORE],
                epochs_column: str = _RE.EPOCHS_COLUMN,
                groups_column: str = _RE.GROUPS_COLUMN) -> Tuple[Smiles, pd.DataFrame, list, list]:
    """
         The load_smiles function loads data from a file and allocates its data to a Smiles object
         and to a score as well as epoch list.

         Parameters
         ----------
         path: str
            path to the file containing the data
         smiles_column: str = "SMILES"
            the file column containing the smiles
         values_columns: str = "total_score"
            the file column containing the total_score
         epochs_column: str = "Step"
            the file column containing the epochs
         groups_column: str = "groups"
            the file column containing the groups

         Returns
         -------
         ChemData
             returns a Tuple object containing a Smiles object as well as score and epoch lists
    """
    def _get_values_df(data_df: pd.DataFrame, column_list: list) -> pd.DataFrame:
        if not isinstance(column_list, list) or len(column_list) < 1:
            return pd.DataFrame()

        columns_for_df = []
        for item in column_list:
            if item in data_df:
                columns_for_df.append(item)
            else:
                print(f"Warning: {item} not found in csv. Please check for typos.")

        if len(columns_for_df) < 1:
            print(f"Warning: No column names remaining, so no values will be stored. "
                  f"(Caution: No 3D plotting possible!).")
            return pd.DataFrame()

        values_df = pd.DataFrame(data_df[columns_for_df])
        return values_df

    loaded_data_df = pd.read_csv(path)
    column_names = list(loaded_data_df)
    smiles = Smiles(list(loaded_data_df[smiles_column]))
    values = _get_values_df(loaded_data_df, values_columns)
    epoch = [] if epochs_column not in column_names else list(loaded_data_df[epochs_column])
    groups = [] if groups_column not in column_names else list(loaded_data_df[groups_column])

    return smiles, values, epoch, groups
