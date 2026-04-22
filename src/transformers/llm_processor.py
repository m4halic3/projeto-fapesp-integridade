import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def processar_com_llama(texto_artigo):
    """
    Realiza a inferência usando Llama 3 para identificar sinais de IA.
    """
    # Carrega configurações do .env
    url = "http://localhost:11434/api/generate"
    model = os.getenv("OLLAMA_MODEL", "llama3.2:1b")
    
    prompt = f"""
    Você é um auditor de integridade científica. Analise o texto abaixo e responda:
    1. Existe uma mudança brusca de estilo ou vocabulário entre o desenvolvimento e a conclusão?
    2. Qual a probabilidade (0-100%) de a conclusão ter sido gerada por um assistente de IA?
    3. O motivo da retratação (se fosse o caso) seria inconsistência estilística?
    Retorne a resposta APENAS em um JSON estruturado.

    Texto: {texto_artigo[:3000]}
    """

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }

    try:
        response = requests.post(url, json=payload, timeout=300)
        response.raise_for_status()
        resultado_bruto = response.json().get("response")
        return json.loads(resultado_bruto)
    except Exception as e:
        return {"erro": f"Erro na inferência Llama: {str(e)}"}