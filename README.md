# Buscador de Artigos Acadêmicos

Um script Python para buscar e baixar automaticamente artigos acadêmicos de várias fontes.

## Funcionalidades

- Busca artigos em múltiplos publishers acadêmicos
- Organiza downloads por tópicos
- Suporta checkpointing para retomar downloads interrompidos
- Gerencia rate limiting e retry automático
- Logging detalhado das operações

## Publishers Suportados

- Frontiers
- MDPI
- Nature
- PLOS
- BioMedCentral
- Hindawi
- SciELO
- Taylor & Francis
- SAGE

## Requisitos

```bash
pip install -r requirements.txt
```

## Como Usar

1. Clone o repositório:
```bash
git clone https://github.com/Dagon67/buscador-de-artigos.git
cd buscador-de-artigos
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute o script:
```bash
python test_scraper.py
```

Os artigos serão baixados na pasta `downloads`, organizados por tópico.

## Estrutura do Projeto

- `test_scraper.py`: Script principal que gerencia as buscas e downloads
- `scraper.py`: Classe principal com a lógica de scraping
- `requirements.txt`: Dependências do projeto

## Tópicos de Busca

- Giftedness (Superdotação)
- Alternative Learning (Aprendizagem Alternativa)
- Historical Figures (Figuras Históricas)
- Brain Topology (Topologia Cerebral)
- Types of Intelligence (Tipos de Inteligência)
- Learning Methods (Métodos de Aprendizagem)
- Interdisciplinary (Interdisciplinar)
- Cultural Dimensions (Dimensões Culturais)
- Metacognition (Metacognição)

## Contribuindo

Sinta-se à vontade para abrir issues ou enviar pull requests com melhorias.

## Licença

MIT License
