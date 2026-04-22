import re

def estruturar_metadados(dados_paginas):
    """Segmenta o texto em seções acadêmicas conforme o projeto FAPESP."""
    texto_completo = " ".join([p["texto"] for p in dados_paginas])
    
    # Seções alvo definidas no seu projeto
    secoes_regras = {
        "resumo": r'(?i)abstract|resumo',
        "introducao": r'(?i)introduction|introdução',
        "metodologia": r'(?i)methods|methodology|metodologia',
        "resultados": r'(?i)results|resultados',
        "conclusao": r'(?i)conclusion|conclusão',
        "referencias": r'(?i)references|referências'
    }

    metadados = {
        "titulo": dados_paginas[0]["texto"].split('\n')[0].strip(),
        "secoes": {}
    }

    # Lógica de "quebra" de seções (Parsing)
    for secao, padrao in secoes_regras.items():
        # Busca o conteúdo entre o nome da seção e a próxima seção provável
        regex = f"{padrao}[:\s]*(.*?)(?=\s*(?:{'|'.join(secoes_regras.values())}|$))"
        match = re.search(regex, texto_completo, re.DOTALL | re.IGNORECASE)
        metadados["secoes"][secao] = match.group(1).strip() if match else "Não identificado"

    return metadados