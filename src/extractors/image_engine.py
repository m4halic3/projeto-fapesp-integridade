import fitz
import cv2
import numpy as np
import os

def extrair_e_analisar_imagens(pdf_path, output_dir="data/figures"):
    """Extrai imagens e prepara para análise SIFT (identificação de digitais da imagem)."""
    doc = fitz.open(pdf_path)
    os.makedirs(output_dir, exist_ok=True)
    
    resultados_imagens = []
    
    for i in range(len(doc)):
        for img_index, img in enumerate(doc.get_page_images(i)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            
            # Salva a imagem para conferência
            img_name = f"img_p{i+1}_{img_index}.png"
            img_path = os.path.join(output_dir, img_name)
            with open(img_path, "wb") as f:
                f.write(image_bytes)
            
            # Aqui entrará a lógica do SIFT futuramente
            resultados_imagens.append({"nome": img_name, "caminho": img_path})
            
    return resultados_imagens