import fitz # PyMuPDF

def extrair_texto_bruto(pdf_path):
    """Transforma o PDF em um dicionário estruturado por páginas."""
    try:
        doc = fitz.open(pdf_path)
        paginas = []
        for i, pagina in enumerate(doc):
            paginas.append({
                "numero": i + 1,
                "texto": pagina.get_text("text")
            })
        return paginas
    except Exception as e:
        print(f"Erro na extração de texto: {e}")
        return None