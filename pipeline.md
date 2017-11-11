'http://www.rio.rj.gov.br/web/cgm/tabelas'


carregar_index :: Index
    Um thunk que retorna a tabela com os links parents de cada
    tópico
    
    ex de resultado:
    {
        'Gêneros alimentícios': {
            'url': 'http://www.rio.rj.gov.br/web/cgm/exibeconteudo?id=6636170'
        },
        ...
    }


scrape_todos_links :: Index -> Index
    Para cada parent url, complete as que não tiver entradas 'texto' e 'url'

    ex de resultado:
    {
        'Gêneros alimentícios': {
            'url': 'http://www.rio.rj.gov.br/web/cgm/exibeconteudo?id=6636170'
            'entradas': [
                {'texto': '1ª quinzena de Janeiro',
                  'url': 'http://www.rio.rj.gov.br/dlstatic/10112/6632414/4179629/PRE_TAB_201612Q2portal.pdf'},
                ...
            ]            
        },
        ...
    }


download_todos_pdfs :: (str -> Path) -> Index -> Index
    Para cada entrada em cada parent, checa os que não tem pdf baixado e baixa no Path dado

    {
        'Gêneros alimentícios': {
            'url': 'http://www.rio.rj.gov.br/web/cgm/exibeconteudo?id=6636170'
            'entradas': [
                {'texto': '1ª quinzena de Janeiro',
                  'url': 'http://www.rio.rj.gov.br/dlstatic/10112/6632414/4179629/PRE_TAB_201612Q2portal.pdf'
                  'pdf': '../downloads/generos_alimenticios/PRE_TAB_201612Q2portal.pdf',
                }
                ...
            ]            
        },
        ...
    }


extrair_todas_validade :: Index -> Index
    {
        'Gêneros alimentícios': {
            'url': 'http://www.rio.rj.gov.br/web/cgm/exibeconteudo?id=6636170'
            'entradas': [
                {'texto': '1ª quinzena de Janeiro',
                  'url': 'http://www.rio.rj.gov.br/dlstatic/10112/6632414/4179629/PRE_TAB_201612Q2portal.pdf'
                  'pdf': '../downloads/generos_alimenticios/PRE_TAB_201612Q2portal.pdf',
                  'validade': '2017-05-29/2017-08-30',
                }
                ...
            ]            
        },
        ...
    }


exportar_todos_excel :: (str -> Path) -> Index -> Index
    {
        'Gêneros alimentícios': {
            'url': 'http://www.rio.rj.gov.br/web/cgm/exibeconteudo?id=6636170'
            'entradas': [
                {'texto': '1ª quinzena de Janeiro',
                  'url': 'http://www.rio.rj.gov.br/dlstatic/10112/6632414/4179629/PRE_TAB_201612Q2portal.pdf'
                  'pdf': '../downloads/generos_alimenticios/PRE_TAB_201612Q2portal.pdf',
                  'validade': '2017-05-29/2017-08-30',
                  'excel': '../excels/generos_alimenticios/PRE_TAB_201612Q2portal.xls',
                }
                ...
            ]            
        },
        ...
    }
