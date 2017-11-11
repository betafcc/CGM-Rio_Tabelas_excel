from lib.typing import Url, Path, Index

import re
from datetime import datetime

import pandas as pd
from tabula import read_pdf
from PyPDF2 import PdfFileReader
from scrapetools import scrape

from lib.util import drop_repeated_headers


def scrape_links(url : Url) -> Index:

    return [
        {
            'url': a.attrib['href'],
            'texto': (''
                      .join(a.xpath('.//text()'))
                      .strip()
                      .replace(u'\xa0', u' ')),
        }
        for a in scrape(url, css='table a')
    ]


# Retonar formato padrão ISO8601 de intervalo temporal
def extrair_validade(path : Path) -> str:
    # abre e extrai text da primeira página
    text_p0 = PdfFileReader(path).getPage(0).extractText()

    # retorna parecido com: '16/09/2017    a    30/09/2017'
    validade = re.findall(r'validade.*?(\d.+\d)', text_p0, flags=re.I)[0]

    # ['16/09/2017', 'a', '30/09/2017']
    start, end = validade.split(' a ')
    start = start.replace(' ', '')
    end   = end.replace(' ', '')

    # converte para formato de data ISO8601
    start = datetime.strptime(start, '%d/%m/%Y').strftime('%Y-%m-%d')
    end   = datetime.strptime(end, '%d/%m/%Y').strftime('%Y-%m-%d')

    # junta as duas datas no formato de intervalo ISO8601
    return '/'.join((start, end))


def extrair_df(path : Path) -> pd.DataFrame:
    # print(f'Extraindo df de {path}')
    df = extract_table(path)
    # print('df extraida')
    # print('formatando df....')
    df = format_table(df)
    # print('df formata')
    return df


def extract_table(path : Path) -> pd.DataFrame:
    pandas_options = {
        'dtype': str,
    }

    return read_pdf(
        path,
        pages='all',
        pandas_options=pandas_options,
    )


def format_table(df : pd.DataFrame) -> pd.DataFrame:
    # em alguns pdf, o cabeçalho é repitido em cada página
    # isso joga eles fora
    df = drop_repeated_headers(df)

    # Separe items com ord validos dos outros
    ords     = df[df.ORD.notnull()]
    non_ords = df[df.ORD.isnull()]

    # Assuma que os outros são as descrições, shift up por 1 e renomeie
    # como uma nova coluna 'DESCRIÇÃO'
    descricoes = non_ords
    descricoes.index = non_ords.index - 1
    descricoes = descricoes['GÊNEROS ALIMENTÍCIOS'].rename('DESCRIÇÃO')

    # Alguns rows podem permanecem sem ORD por problema no read_pdf,
    # por isso, concatene pra cima os vazios
    acc = []
    df_isnull = df.ORD.isnull()
    for i, desc in descricoes.items():
        if not df_isnull[i]:
            acc.append((i, desc))
        else:
            acc[-1] = (acc[-1][0], acc[-1][1].strip() + ' ' + desc.strip())

    # Agora recrie a coluna 'DESCRIÇÃO', dessa vez garantido de não ter um
    # sem ORD
    ixs, descs = zip(*acc)
    new_descricoes = pd.Series(descs, index=ixs, name='DESCRIÇÃO')

    return pd.concat(
        [ords, new_descricoes],
        axis=1,
    )
