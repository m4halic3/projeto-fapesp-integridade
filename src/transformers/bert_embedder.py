import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
import os

class BertEmbedder:
    def __init__(self):
        model_name = os.getenv("BERT_MODEL", "bert-base-uncased")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

    def gerar_embedding(self, texto):
        """Cria o vetor numérico (Embedding) que representa o sentido do texto."""
        if not texto or len(texto) < 20: return None
        
        inputs = self.tokenizer(texto, return_tensors='pt', truncation=True, max_length=512, padding=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        # O embedding é a média da última camada oculta (Mean Pooling)
        return outputs.last_hidden_state.mean(dim=1).numpy().tolist() # Converte para lista para salvar no Mongo

    def calcular_similaridade(self, emb1, emb2):
        """Mede o quão parecidos são dois textos (0 a 1)."""
        return float(cosine_similarity([emb1], [emb2])[0][0])