import os
import json
from pathlib import Path
from datetime import datetime
from src.database.mongo_manager import MongoManager
from src.extractors.pdf_engine import extrair_texto_bruto
from src.extractors.image_engine import extrair_e_analisar_imagens
from src.transformers.bert_embedder import BertEmbedder

def executar():
    db = MongoManager()
    bert = BertEmbedder()
    raw_dir = Path("data/raw")
    
    for pdf in raw_dir.glob("*.pdf"):
        print(f"--- Iniciando Perícia: {pdf.name} ---")
        
        # 1. Extração de Texto e Imagens
        texto_paginas = extrair_texto_bruto(pdf)
        imagens_extraidas = extrair_e_analisar_imagens(pdf)
        
        # 2. Geração de DNA Textual (Embedding do Resumo e Conclusão)
        resumo_text = texto_paginas[0]["texto"] if texto_paginas else ""
        conclusao_text = texto_paginas[-1]["texto"] if texto_paginas else ""
        
        emb_resumo = bert.gerar_embedding(resumo_text)
        emb_conclusao = bert.gerar_embedding(conclusao_text)
        
        score_interno = 0
        if emb_resumo and emb_conclusao:
            score_interno = bert.calcular_similaridade(emb_resumo[0], emb_conclusao[0])

        # 3. Consolidação dos Dados (Prontos para cruzar com OpenAlex/RetractionWatch)
        dados_pericia = {
            "arquivo": pdf.name,
            "data_pericia": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "assinatura_embeddings": {
                "resumo": emb_resumo,
                "conclusao": emb_conclusao,
                "similaridade_interna": score_interno
            },
            "imagens_detectadas": imagens_extraidas,
            "texto_completo": texto_paginas,
            "status_auditoria": "Aguardando cruzamento com robôs externos"
        }

        # 4. Persistência
        db.salvar_analise(dados_pericia)
        print(f"✅ Perícia concluída e salva no MongoDB.")

if __name__ == "__main__":
    executar()