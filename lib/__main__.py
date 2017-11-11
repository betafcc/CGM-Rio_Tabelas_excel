from typing import Dict, Tuple

import json
from copy import deepcopy
from os.path import dirname
from concurrent.futures import ThreadPoolExecutor as Pool

from lib.por_topico import (
    scrape_links_topico,
    download_pdfs_topico,
    extrair_validades_topico,
    exportar_excels_topico,
)
from lib.util import mkdirdeep
from lib.configuration import configuration


def carregar_index() -> Dict:
    try:
        with open(configuration['index_path'], 'r') as fp:  # type: ignore
            return json.load(fp)
    except FileNotFoundError:
        return configuration['default_index']  # type: ignore


def scrape_todos_links(index: Dict) -> Dict:
    index = deepcopy(index)

    def mapper(k: str, v: Dict) -> Tuple[str, Dict]:
        scraper = configuration['scrape_links'](k)  # type: ignore
        return k, scrape_links_topico(v, scraper=scraper)

    print('Scraping links de:\n\t' + "\n\t".join(index))
    with Pool(10) as executor:
        return dict(
            executor.map(mapper, *zip(*index.items()))
        )


def download_todos_pdfs(index: Dict) -> Dict:
    index = deepcopy(index)

    for nome, topico in index.items():
        index[nome] = download_pdfs_topico(
            topico,
            destino=configuration['pdfs'](nome),  # type: ignore
            nome=nome,
        )

    return index


def extrair_todas_validades(index: Dict) -> Dict:
    index = deepcopy(index)

    for nome, topico in index.items():
        index[nome] = extrair_validades_topico(
            topico,
            extrator=configuration['extrair_validade'](nome),  # type: ignore
            nome=nome,
        )

    return index


def exportar_todos_excels(index: Dict) -> Dict:
    index = deepcopy(index)

    for nome, topico in index.items():
        index[nome] = exportar_excels_topico(
            topico,
            extrator=configuration['extrair_df'](nome),  # type:ignore
            destino=configuration['excels'](nome),  # type: ignore
            nome=nome,
        )

    return index


def salvar_index(index: Dict) -> None:
    dest = configuration['index_path']
    mkdirdeep(dirname(dest))  # type: ignore

    with open(dest, 'w') as fp:  # type: ignore
        json.dump(index,
                  fp,
                  ensure_ascii=False,
                  indent=4,
                  sort_keys=True)


if __name__ == '__main__':
    index = carregar_index()
    index = scrape_todos_links(index)
    salvar_index(index)
    index = download_todos_pdfs(index)
    salvar_index(index)
    index = extrair_todas_validades(index)
    salvar_index(index)
    index = exportar_todos_excels(index)
    salvar_index(index)
