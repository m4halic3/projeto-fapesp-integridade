import json
from pathlib import Path
from datetime import datetime

# Importação dos motores do projeto
from src.extractors.pdf_engine import extrair_texto_bruto
from src.extractors.openalex_engine import consultar_openalex_por_titulo
from src.transformers.llm_processor import processar_com_llama
from src.transformers.bert_embedder import processar_json_com_bert

def executar():
    raw_dir = Path("data/raw")
    processed_dir = Path("data/processed")
    processed_dir.mkdir(parents=True, exist_ok=True)

    # Itera sobre todos os PDFs na pasta raw
    for pdf in raw_dir.glob("*.pdf"):
        print(f"\n{'='*50}")
        print(f"Iniciando Pipeline: {pdf.name}")
        print(f"{'='*50}")
        
        # 1. Extração de Texto Bruto
        texto_paginas = extrair_texto_bruto(pdf)
        if not texto_paginas:
            print(f"Erro: Não foi possível extrair texto de {pdf.name}")
            continue

        # 2. Consulta de Metadados Externos (OpenAlex)
        # Tentamos pegar a primeira linha (geralmente o título) para a busca
        titulo_busca = texto_paginas[0]["texto"].split('\n')[0].strip()
        metadados_externos = consultar_openalex_por_titulo(titulo_busca)

        # 3. Preparação do Contexto para o LLM (Llama 3)
        # Resumo (Página 1) vs Conclusão (Última Página)
        resumo_referencia = texto_paginas[0]["texto"][:2500] 
        conclusao_teste = texto_paginas[-1]["texto"][-2500:] 
        
        contexto_prompt = f"RESUMO (REFERÊNCIA):\n{resumo_referencia}\n\nCONCLUSÃO (TESTE):\n{conclusao_teste}"
        
        print("-> Gerando análise qualitativa (Llama 3.2 1B)...")
        analise_qualitativa = processar_com_llama(contexto_prompt)

        # 4. Estruturação do Dicionário de Dados
        dados_finais = {
            "arquivo": pdf.name,
            "ultima_analise": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "metadados_api": metadados_externos,
            "diagnostico_ia": analise_qualitativa,
            "estrutura_documento": texto_paginas 
        }

        # 5. Salvamento do JSON Intermediário
        output_file = processed_dir / f"{pdf.stem}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(dados_finais, f, ensure_ascii=False, indent=4)
        
        # 6. Processamento Quantitativo (BERT)
        # O BERT lê o arquivo salvo, calcula a similaridade e atualiza o JSON
        print("-> Calculando similaridade vetorial (BERT)...")
        processar_json_com_bert(output_file)
        
        print(f"\nProcessamento concluído: {output_file.name}")
        print(f"{'='*50}\n")

if __name__ == "__main__":
    executar()