from os.path import abspath, join, dirname
__dirname = abspath(dirname(__file__))

import json
from datetime import datetime
from urllib.parse import urljoin
from posixpath import basename

import pandas as pd
from tabulate import tabulate

from convert_relative_paths import REL_INDEX


TEMPLATE = join(__dirname, 'README_template.md')
README   = join(__dirname, '..', 'README.md')
DATA_PREFIX = 'https://github.com/betafcc/CGM-Rio_Tabelas_excel/raw/master/data/'


def main():
    index = load_json(REL_INDEX)
    template = load_template(TEMPLATE)

    with open(README, 'w') as file:
        file.write(format_template(index, template))


def load_json(path):
    with open(path, 'r') as file:
        return json.load(file)


def load_template(path):
    with open(path, 'r') as file:
        return file.read()


def format_template(index, template):
    d = {}
    for titulo, topico in index.items():
        url = topico['url']

        d.update({
            f'url_{titulo}': f'[{titulo}]({url})',
            f'entradas_{titulo}': to_markdown(topico['entradas']),
        })

    return template.format(**d)


def to_markdown(entradas):
    return tabulate(
        format_table(entradas),
        showindex=False,
        headers='keys',
        tablefmt='pipe'
    )


def format_table(entradas):
    df = (pd
        .DataFrame(entradas)
        .drop('pdf', axis=1)
        .rename(columns={
            'url': 'Original',
            'excel': 'Excel',
            'texto': 'Descrição',
            'validade': 'Validade',
        })
        [['Descrição', 'Validade', 'Excel', 'Original']]
    )

    df.Excel = df.Excel.map(format_excel)
    df.Original = df.Original.map(format_pdf)
    df.Validade = df.Validade.map(format_validade)

    return df


def format_excel(path):
    download_url = urljoin(DATA_PREFIX, path)
    name = basename(download_url)

    return f'[{name}]({download_url})'


def format_pdf(path):
    name = basename(path)

    return f'[{name}]({path})'


def format_validade(validade):
    validade = validade.split('/')
    validade = [
        datetime
        .strptime(val, '%Y-%m-%d')
        .strftime('%d/%m/%Y')
        for val in validade
    ]

    return ' a '.join(validade)


if __name__ == '__main__':
    main()
