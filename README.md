# Pré-Processamento de Artigos Científicos Retratados Utilizando Aprendizado de Máquina


## 1. Descrição do Projeto

Este repositório contém a implementação da **pipeline de software** descrita no projeto de Iniciação Científica submetido à **FAPESP**. A pesquisa foca no desenvolvimento de métodos computacionais para a extração, processamento e análise de metadados e conteúdo textual de artigos científicos retratados ou sob suspeita de má conduta científica.

O sistema utiliza técnicas avançadas de **Processamento de Linguagem Natural (NLP)** e **Aprendizado de Máquina** para identificar padrões atípicos que caracterizam publicações fraudulentas, tais como:

* **Disparidades estilísticas:** Comparação entre diferentes seções do documento (ex: Resumo autoral vs. Conclusão sintética).
* **Assinaturas Digitais de LLMs:** Identificação de vestígios linguísticos deixados por modelos de linguagem de grande escala.
* **Análise de Metadados:** Verificação da consistência e proveniência das informações do artigo.
--- 

## 2. Arquitetura do Sistema
O projeto foi estruturado de forma modular e extensível, permitindo a reprodutibilidade dos experimentos conforme as diretrizes de Ciência Aberta.

**Estrutura de Arquivos**
```text
projeto_fapesp/
├── pipeline_main.py
├── data/
│   ├── raw/
│   └── processed/
└── src/
    ├── extractors/
    │   └── pdf_engine.py
    └── transformers/
        ├── llm_processor.py
        └── bert_embedder.py
```

* **`pipeline_main.py`**: Script principal (orquestrador) responsável por coordenar o fluxo de dados do sistema, desde a leitura dos arquivos brutos até a geração dos relatórios finais (**Extração → Processamento → Persistência**).
* **`src/extractors/`**: Contém os módulos de infraestrutura para o *parsing* técnico.
    * `pdf_engine.py`: Motor de extração baseado na biblioteca **PyMuPDF**, otimizado para preservar a integridade semântica de artigos científicos.
* **`src/transformers/`**: Motores de Inteligência Artificial e Processamento de Linguagem Natural:
    * `llm_processor.py`: Executa a análise qualitativa, utilizando o modelo **Llama 3** para identificar marcas d'água linguísticas e extrair *insights* sobre a autoria.
    * `bert_embedder.py`: Responsável pela análise quantitativa, gerando **Embeddings** (vetores de alta dimensionalidade) para detecção de anomalias estatísticas e busca vetorial.
* **`data/`**: Camada de armazenamento de dados:
    * `raw/`: Diretório de entrada contendo os arquivos PDF originais submetidos à análise.
    * `processed/`: Repositório de saída com os resultados estruturados em formato **JSON**, permitindo auditoria e futuras visualizações de dados.
