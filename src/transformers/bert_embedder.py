from transformers import BertTokenizer, BertModel
import torch

class BertEmbedder:
    def __init__(self):
        # Carregando o modelo pré-treinado (ex: bert-base-multilingual para português/inglês)
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
        self.model = BertModel.from_pretrained('bert-base-multilingual-cased')

    def gerar_embedding(self, texto):
        # Transforma o texto em tokens e depois em tensores
        inputs = self.tokenizer(texto, return_tensors='pt', truncation=True, max_length=512, padding='max_length')
        
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        # O embedding da frase é geralmente a média da última camada oculta
        embeddings = outputs.last_hidden_state.mean(dim=1)
        return embeddings.numpy().tolist()[0] # Retorna uma lista de números (vetor)