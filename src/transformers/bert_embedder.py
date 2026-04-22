import json
import torch
import os
from pathlib import Path
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv

load_dotenv()

class BertEmbedder:
    def __init__(self):
        model_name = os.getenv("BERT_MODEL", "bert-base-uncased")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

    def _get_embedding(self, text):
        inputs = self.tokenizer(text, return_tensors='pt', 
                                truncation=True, max_length=512, padding=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).numpy()

    def calcular_similaridade(self, resumo, conclusao):
        if not resumo or not conclusao: return 0.0
        vec_resumo = self._get_embedding(resumo)
        vec_conclusao = self._get_embedding(conclusao)
        score = cosine_similarity(vec_resumo, vec_conclusao)[0][0]
        return round(float(score), 4)

def processar_json_com_bert(json_path):
    """Lê o JSON, calcula a similaridade e retorna o dicionário atualizado."""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    resumo = ""
    conclusao = ""
    
    for pag in data.get('estrutura_documento', []):
        if pag['numero'] == 1: resumo = pag['texto']
        # Pega a última página dinamicamente se não houver a página 7
        if pag['numero'] == len(data.get('estrutura_documento', [])):
            conclusao = pag['texto']

    embedder = BertEmbedder()
    score = embedder.calcular_similaridade(resumo, conclusao)

    data['analise_quantitativa'] = {
        "metodo": "BERT Base Uncased",
        "similaridade_cosseno": score,
        "alerta_anomalia": score < 0.45
    }

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    return data # Retorna para o pipeline salvar no MongoDB