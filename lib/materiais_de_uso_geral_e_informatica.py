from typing import Tuple, List
from lib.typing import Path

import pandas as pd
from tabula import read_pdf

from lib.util import drop_repeated_headers, take_consecutive


def extrair_df(path : Path) -> List[Tuple[str, pd.DataFrame]]:
    # print(f'Extraindo df de {path}')
    df = extract_table(path)
    # print('df extraida')
    # print('formatando df....')
    df = format_table(df)
    # print('df formatada')
    return df


def extract_table(path: Path) -> pd.DataFrame:
    pandas_options = {
        'dtype': str,
        'header': None,
        'names': ['N°',  'CÓDIGO', 'Materiais Diversos', 'Unid', 'R$ Preço'],
    }

    return read_pdf(
        path,
        spreadsheet=True,
        pandas_options=pandas_options,
        pages='all',
    )


def format_table(df: pd.DataFrame,
                 ) -> List[Tuple[str, pd.DataFrame]]:
    df = drop_repeated_headers(df)

    nans = df[df.columns[1]].isnull()
    nan_indexes = df[nans].index

    if len(nan_indexes):
        start, *_, stop = take_consecutive(nan_indexes)

        return [
            ('Uso Geral', df.iloc[:start]),
            ('Informática', df.iloc[stop + 1:].reset_index(drop=True)),
        ]

    else:
        _, index = df[df[df.columns[0]] == '1'].index
        return [
            ('Uso Geral', df.iloc[:index]),
            ('Informática', df.iloc[index:].reset_index(drop=True)),
        ]
