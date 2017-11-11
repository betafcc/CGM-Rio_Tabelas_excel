from typing import Dict, Callable, List, Union, Iterable
from lib.typing import Path
from concurrent.futures import Executor

import asyncio
from copy import deepcopy
from os.path import join
from concurrent.futures import ThreadPoolExecutor as Pool

import pandas as pd
from tqdm import tqdm
from scrapetools import download_sync
from scrapetools.util import url_basename

from lib.util import mkdirdeep, to_excel, sensible_export_path


def scrape_links_topico(topico  : Dict,
                        scraper : Callable[[str], List[Dict]],
                        ) -> Dict:
    topico = deepcopy(topico)

    # Scrape
    scraped = scraper(topico['url'])

    # Check the record if already set
    entradas = topico.get('entradas')

    if not entradas:
        topico['entradas'] = scraped
    # else, use the 'url' attribute in each entry as the id
    # to prevent duplicate entries
    else:
        urls = set([a['url'] for a in entradas])
        scraped = [a
                   for a in scraped
                   if a['url'] not in urls]
        for a in scraped:
            topico['entradas'].append(a)

    return topico


def download_pdfs_topico(topico  : Dict,
                         destino : Path,
                         nome    : str,
                         ) -> Dict:
    topico = deepcopy(topico)
    to_download = [
        entrada
        for entrada in topico['entradas']
        if not entrada.get('pdf')
    ]

    if not to_download:
        return topico

    mkdirdeep(destino)

    print(f'Baixando pdfs de {nome}')
    download_sync(map(lambda a: a['url'], to_download),
                  destino,
                  show_progress=True)

    for entrada in to_download:
        entrada['pdf'] = join(destino, url_basename(entrada['url']))

    return topico


def extrair_validades_topico(topico   : Dict,
                             extrator : Callable[[Path], str],
                             nome     : str,
                             ) -> Dict:
    topico = deepcopy(topico)
    loop   = asyncio.get_event_loop()
    to_extract = [
        entrada
        for entrada in topico['entradas']
        if not entrada.get('validade')
    ]

    if not to_extract:
        return topico

    async def target(executor : Executor,
                     entrada  : Dict,
                     pbar     : tqdm,
                     ) -> None:
        await loop.run_in_executor(executor, thread_target, entrada)
        pbar.update(1)

    def thread_target(entrada: Dict) -> None:
        entrada['validade'] = correct(extrator(entrada['pdf']))

    # Algumas validades tem typos do tipo:
    # 16 quando devia ser 2016
    def correct(val: str) -> str:
        if val.startswith('16'):
            return '20' + val
        return val

    print(f'Extraindo validades de {nome}')
    with Pool(10) as executor, tqdm(total=len(to_extract),
                                    desc='Overall',
                                    unit='file') as pbar:
            loop.run_until_complete(asyncio.gather(
                *(target(executor, entrada, pbar)
                  for entrada in to_extract)
            ))

    return topico


def exportar_excels_topico(topico   : Dict,
                           extrator : Callable[[Path], Union[pd.DataFrame,
                                                             Iterable[pd.DataFrame]]],
                           destino  : Path,
                           nome     : str,
                           ) -> Dict:
    topico = deepcopy(topico)
    loop   = asyncio.get_event_loop()
    to_extract = [
        entrada
        for entrada in topico['entradas']
        if not entrada.get('excel')
    ]

    if not to_extract:
        return topico

    mkdirdeep(destino)

    async def target(executor : Executor,
                     entrada  : Dict,
                     destino  : Path,
                     pbar     : tqdm,
                     ) -> None:
        await loop.run_in_executor(executor, thread_target, entrada)
        pbar.update(1)

    def thread_target(entrada : Dict) -> None:
        df = extrator(entrada['pdf'])
        excel_path = sensible_export_path(entrada['pdf'], destino, '.xls')
        # print(f'Will export to {excel_path}')
        to_excel(df, excel_path)
        # print('Exported')
        entrada['excel'] = excel_path

    print(f'Extraindo tabelas de {nome}')
    with Pool(3) as executor, tqdm(total=len(to_extract),
                                   desc='Overall',
                                   unit='file') as pbar:
        loop.run_until_complete(asyncio.gather(
            *(target(executor, entrada, destino, pbar)
              for entrada in to_extract)
        ))

    return topico
