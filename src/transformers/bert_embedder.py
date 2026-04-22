import json
import torch
from pathlib import Path
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity

class BertEmbedder:
    def __init__(self, model_name='bert-base-uncased'):
        print(f"--- Carregando modelo {model_name} ---")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

    def _get_embedding(self, text):
        """Transforma uma string em um vetor numérico (tensor)."""
        inputs = self.tokenizer(text, return_tensors='pt', 
                                truncation=True, max_length=512, padding=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        # Usamos a média da última camada oculta como representação do texto (Mean Pooling)
        return outputs.last_hidden_state.mean(dim=1).numpy()

    def calcular_similaridade(self, resumo, conclusao):
        """Calcula a similaridade de cosseno entre duas strings."""
        if not resumo or not conclusao:
            return 0.0
            
        vec_resumo = self._get_embedding(resumo)
        vec_conclusao = self._get_embedding(conclusao)
        
        # Similaridade de cosseno retorna um valor entre -1 e 1
        score = cosine_similarity(vec_resumo, vec_conclusao)[0][0]
        return round(float(score), 4)

def processar_json_com_bert(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Lógica de extração baseada na estrutura do seu PDF (Página 1 e Página 7)
    # Nota: Ajustamos o índice (0-based) se necessário
    resumo = ""
    conclusao = ""
    
    for pag in data.get('estrutura_documento', []):
        if pag['numero'] == 1:
            resumo = pag['texto']
        if pag['numero'] == 7: # Conforme seu JSON gerado
            conclusao = pag['texto']

    embedder = BertEmbedder()
    score = embedder.calcular_similaridade(resumo, conclusao)

    # Adiciona o resultado quantitativo ao JSON original
    data['analise_quantitativa'] = {
        "metodo": "BERT Base Uncased",
        "similaridade_cosseno": score,
        "alerta_anomalia": score < 0.45  # Threshold sugerido para IC
    }

    # Salva o JSON atualizado
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f"--- Sucesso! Similaridade BERT: {score} ---")

if __name__ == "__main__":
    # Teste rápido apontando para o seu arquivo processado
    path = Path("data/processed/artigo_electrosfiCSBC.json")
    if path.exists():
        processar_json_com_bert(path)