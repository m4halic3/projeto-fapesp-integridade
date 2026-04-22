import json
from pathlib import Path
from datetime import datetime

# O ponto antes de extractors e transformers resolve o erro de módulo
from src.extractors.pdf_engine import extrair_texto_bruto
from src.transformers.llm_processor import processar_com_llama
from src.transformers.bert_embedder import processar_json_com_bert

def executar():
    raw_dir = Path("data/raw")
    processed_dir = Path("data/processed")
    processar_json_com_bert("data/processed/artigo_electrosfiCSBC.json")
    processed_dir.mkdir(parents=True, exist_ok=True)

    for pdf in raw_dir.glob("*.pdf"):
        print(f"Analisando Integridade: {pdf.name}")
        
        texto_paginas = extrair_texto_bruto(pdf)
        if not texto_paginas: continue

        # ISOLAMENTO PARA TESTE (HUMANO vs IA)
        resumo_humano = texto_paginas[0]["texto"][:2000] 
        conclusao_ia = texto_paginas[-1]["texto"][-2000:] 
        
        # PROMPT COMPARATIVO
        contexto = f"RESUMO (REFERÊNCIA):\n{resumo_humano}\n\nCONCLUSAO (TESTE):\n{conclusao_ia}"
        
        print("Gerando análise comparativa (Llama 3)...")
        analise_ia = processar_com_llama(contexto)

        dados_finais = {
            "arquivo": pdf.name,
            "ultima_analise": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "diagnostico_ia": analise_ia,
            "estrutura_documento": texto_paginas 
        }

        # SOBRESCRITA GARANTIDA PARA ATUALIZAÇÃO DE DADOS
        output_file = processed_dir / f"{pdf.stem}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(dados_finais, f, ensure_ascii=False, indent=4)
        
        print(f"Resultados atualizados em: {output_file.name}\n")

if __name__ == "__main__":
    executar()