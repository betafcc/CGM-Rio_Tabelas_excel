from os.path import join, dirname, abspath

from slugify import slugify

from lib import (
    generos_alimenticios,
    materiais_de_uso_geral_e_informatica,
    catalogo_de_servicos_diversos,
)
from lib.generos_alimenticios import scrape_links, extrair_validade


__dirname = abspath(dirname(__file__))
DATA = abspath(join(__dirname, '..', 'data'))


configuration = {
    'index_path'  : join(DATA, 'index.json'),
    'pdfs'   : lambda topico: join(DATA,   'pdfs', slugify(topico)),
    'excels' : lambda topico: join(DATA, 'excels', slugify(topico)),

    'scrape_links': lambda topico: scrape_links,  # funciona igual pra todos
    'extrair_validade': lambda topico: extrair_validade,  # funciona igual pra todos
    'extrair_df': lambda topico: {
        'Gêneros Alimentícios':
            generos_alimenticios.extrair_df,
        'Materiais de Uso Geral e Informática':
            materiais_de_uso_geral_e_informatica.extrair_df,
        'Catálogo de Serviços Diversos':
            catalogo_de_servicos_diversos.extrair_df,
    }[topico],

    'default_index':  {
        'Gêneros Alimentícios': {
            'url': 'http://www.rio.rj.gov.br/web/cgm/exibeconteudo?id=6636170',
        },
        'Materiais de Uso Geral e Informática': {
            'url': 'http://www.rio.rj.gov.br/web/cgm/exibeconteudo?id=5793020',
        },
        'Catálogo de Serviços Diversos': {
            'url': 'http://www.rio.rj.gov.br/web/cgm/exibeconteudo?id=6607937',
        },
    }
}
