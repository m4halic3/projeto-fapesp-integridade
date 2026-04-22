import requests
import time

def consultar_openalex_por_titulo(titulo):
    """
    Consulta a API do OpenAlex para obter metadados de um artigo pelo título.
    """
    base_url = "https://api.openalex.org/works"
    # O OpenAlex recomenda usar um e-mail no 'mailto' para entrar na "polite pool"
    params = {
        'filter': f'title.search:{titulo}',
        'mailto': 'teu_email@ifsp.edu.br' 
    }

    try:
        print(f"--- Consultando OpenAlex: {titulo[:50]}... ---")
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            results = response.json().get('results', [])
            if results:
                # Pegamos o primeiro resultado mais relevante
                work = results[0]
                return {
                    "oa_id": work.get('id'),
                    "doi": work.get('doi'),
                    "is_retracted": work.get('is_retracted'),
                    "cited_by_count": work.get('cited_by_count'),
                    "topics": [t.get('display_name') for t in work.get('topics', [])],
                    "publication_year": work.get('publication_year')
                }
        return None
    except Exception as e:
        print(f"Erro na consulta OpenAlex: {e}")
        return None

if __name__ == "__main__":
    # Teste rápido
    res = consultar_openalex_por_titulo("ElectrosFI: Abstraindo a Complexidade de Hardware")
    print(res)