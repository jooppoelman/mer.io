import os
from typing import Dict, List, Generator
from pandas import DataFrame

from src.models.dataframe_model import DataFrameModel
import pandas as pd


def mock_tact_scenario(mer_data: Dict[str, DataFrameModel], unique_refs: List[str]) -> Dict[str, DataFrameModel]:
    if 'TACTICAL_SCENARIO' not in mer_data:
        mer_data['TACTICAL_SCENARIO'] = DataFrameModel(DataFrame({'REFERENCE': []}), 'TACTICAL_SCENARIO')
    for ref in unique_refs:
        tact_scenario: DataFrame = mer_data['TACTICAL_SCENARIO'].original_df
        if ref not in list(tact_scenario['REFERENCE'].unique()):
            mer_data['TACTICAL_SCENARIO'].original_df = \
                mer_data['TACTICAL_SCENARIO'].original_df.append(
                    pd.DataFrame({
                        'GRID CENTER LAT': [0],
                        'GRID CENTER LONG': [0],
                        'REFERENCE': [ref]
                    }), ignore_index=True)

    return mer_data


def get_valid_files_from_folder(path: str) -> Generator:
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(('.txt', '.zip')):
                yield os.path.join(root, file)