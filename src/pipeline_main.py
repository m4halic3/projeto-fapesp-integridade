import json
from pathlib import Path
from extractors.pdf_engine import extrair_texto_bruto
from transformers.llm_processor import processar_com_llama

def executar():
    raw_dir = Path("data/raw")
    processed_dir = Path("data/processed")
    processed_dir.mkdir(parents=True, exist_ok=True)

    for pdf in raw_dir.glob("*.pdf"):
        print(f"📄 Processando: {pdf.name}")
        
        # 1. Extração via PyMuPDF
        texto_paginas = extrair_texto_bruto(pdf)
        if not texto_paginas: 
            continue

        # --- Lógica para o teste de "IA na Conclusão" ---
        # Pegamos o texto da primeira página (Resumo Humano) 
        # e da última página (Conclusão com IA)
        resumo_humano = texto_paginas[0]["texto"][:2000] # Limita para evitar timeout
        conclusao_ia = texto_paginas[-1]["texto"][-2000:] # Pega o final do arquivo
        
        # Criamos um contexto específico para o Llama analisar a diferença
        texto_para_analise = f"RESUMO (AUTORAL):\n{resumo_humano}\n\nCONCLUSAO (IA):\n{conclusao_ia}"
        
        # 2. Inteligência Artificial via Llama
        # Linha original comentada conforme solicitado:
        # resumo_texto = texto_paginas[0]["texto"]
        
        print("🤖 Solicitando análise comparativa ao Llama...")
        # Agora enviamos o texto otimizado (Resumo + Conclusão)
        analise_ia = processar_com_llama(texto_para_analise)

        # 3. Consolidação dos Metadados
        dados_finais = {
            "arquivo": pdf.name,
            "metadados_ia": analise_ia,
            "conteudo_completo": texto_paginas # Mantém a leitura de todas as páginas
        }

        # 4. Salvamento
        output_file = processed_dir / f"{pdf.stem}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(dados_finais, f, ensure_ascii=False, indent=4)
        
        print(f"✅ JSON gerado em data/processed/{pdf.stem}.json\n")

if __name__ == "__main__":
    executar()