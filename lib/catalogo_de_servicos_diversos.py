from lib.typing import Path

import pandas as pd
from tabula import read_pdf

from lib.util import drop_repeated_headers


def extrair_df(path : Path) -> pd.DataFrame:
    # print(f'Extraindo df de {path}')
    df = extract_table(path)
    # print('df extraida')
    # print('formatando df....')
    df = format_table(df)
    # print('df formata')
    return df


def extract_table(path: Path) -> pd.DataFrame:
    pandas_options = {
        'dtype': str,
    }

    return read_pdf(
        path,
        spreadsheet=True,
        pandas_options=pandas_options,
        pages='all',
    )


def format_table(df: pd.DataFrame,
                 ) -> pd.DataFrame:
    return drop_repeated_headers(df)
