import requests
import json

def processar_com_llama(texto_artigo):
    """
    Realiza a inferência usando Llama 3 para identificar o motivo da retratação.
    """
    url = "http://localhost:11434/api/generate"
    
    # Prompt focado em integridade científica (Recod.AI)
    prompt = f"""
    Você é um auditor de integridade científica. Analise o texto abaixo e responda:
    1. Existe uma mudança brusca de estilo ou vocabulário entre o desenvolvimento e a conclusão?
    2. Qual a probabilidade (0-100%) de a conclusão ter sido gerada por um assistente de IA?
    3. O motivo da retratação (se fosse o caso) seria inconsistência estilística?
    Retorne a resposta APENAS em um JSON estruturado.

    Texto: {texto_artigo[:3000]}
    """

    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }

    try:
        response = requests.post(url, json=payload, timeout=300)
        resultado = response.json().get("response")
        return json.loads(resultado)
    except Exception as e:
        return {"erro": f"Llama offline ou erro de conexão: {str(e)}"}