import fitz

def extrair_texto_bruto(caminho_pdf):
    """Extrai texto de todas as páginas e retorna uma lista."""
    try:
        doc = fitz.open(caminho_pdf)
        paginas = [{"numero": i+1, "texto": p.get_text()} for i, p in enumerate(doc)]
        doc.close()
        return paginas
    except Exception as e:
        print(f"Erro ao abrir PDF {caminho_pdf}: {e}")
        return None