import json
import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Importação dos módulos internos
from src.extractors.pdf_engine import extrair_texto_bruto
from src.extractors.openalex_engine import consultar_openalex_por_titulo
from src.transformers.llm_processor import processar_com_llama
from src.transformers.bert_embedder import processar_json_com_bert
from src.database.mongo_manager import MongoManager

load_dotenv()

def executar():
    # Inicializa o Banco de Dados (Porta 27018 conforme .env)
    db = MongoManager()
    
    raw_dir = Path("data/raw")
    processed_dir = Path("data/processed")
    processed_dir.mkdir(parents=True, exist_ok=True)

    for pdf in raw_dir.glob("*.pdf"):
        print(f"\n--- Processando: {pdf.name} ---")
        
        # 1. Extração
        texto_paginas = extrair_texto_bruto(pdf)
        if not texto_paginas: continue

        # 2. Metadados API
        titulo_busca = texto_paginas[0]["texto"].split('\n')[0].strip()
        metadados_externos = consultar_openalex_por_titulo(titulo_busca)

        # 3. Qualitativo (Llama)
        contexto = f"RESUMO: {texto_paginas[0]['texto'][:2000]}\nCONCLUSÃO: {texto_paginas[-1]['texto'][-2000:]}"
        analise_llama = processar_com_llama(contexto)

        # 4. Estrutura Inicial
        dados_finais = {
            "arquivo": pdf.name,
            "ultima_analise": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "metadados_api": metadados_externos,
            "diagnostico_ia": analise_llama,
            "estrutura_documento": texto_paginas 
        }

        # 5. Salvamento temporário para o BERT processar
        output_file = processed_dir / f"{pdf.stem}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(dados_finais, f, ensure_ascii=False, indent=4)
        
        # 6. Quantitativo (BERT) + Atualização MongoDB
        print("-> Calculando similaridade BERT...")
        dados_completos = processar_json_com_bert(output_file)
        
        print("-> Salvando no MongoDB (IntegrityScan)...")
        db.salvar_analise(dados_completos)
        
        print(f"Sucesso: {pdf.name}")

if __name__ == "__main__":
    executar()