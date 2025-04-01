# Treino Mira

Aplicação Python para treinamento de precisão e reflexos, com diferentes modos de treino e tracking de performance.

## Recursos

- Interface gráfica intuitiva
- Múltiplos modos de treino:
  - Precisão estática
  - Alvos móveis
  - Reflexos rápidos
  - Modo desafio
- Tracking de performance
- Estatísticas detalhadas
- Configurações personalizáveis
- Feedback visual e sonoro

## Tecnologias

- Python 3.8+
- Pygame
- NumPy
- Pandas (para estatísticas)
- PyQt5 (interface gráfica)

## Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/Dagon67/treino-mira.git
cd treino-mira
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso

Execute o programa principal:
```bash
python main.py
```

### Modos de Treino

1. **Precisão Estática**
   - Alvos fixos em posições aleatórias
   - Foco em precisão

2. **Alvos Móveis**
   - Alvos em movimento
   - Treino de tracking

3. **Reflexos Rápidos**
   - Alvos que aparecem e desaparecem rapidamente
   - Melhora do tempo de reação

4. **Modo Desafio**
   - Combinação de diferentes tipos de alvos
   - Dificuldade progressiva

## Configurações

Ajuste as configurações em `config.py`:
- Sensibilidade do mouse
- Tamanho dos alvos
- Velocidade dos alvos móveis
- Duração das sessões
- Cores e sons

## Estatísticas

O programa mantém registro de:
- Precisão por sessão
- Tempo médio de reação
- Progresso ao longo do tempo
- Pontuação em cada modo
- Histórico de sessões

## Estrutura do Projeto

```
treino-mira/
├── src/
│   ├── modes/
│   ├── utils/
│   ├── ui/
│   └── stats/
├── assets/
│   ├── sounds/
│   └── images/
├── config.py
├── main.py
└── README.md
```

## Contribuindo

1. Fork o projeto
2. Crie sua Feature Branch (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a Branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

## Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

## Contato

Seu Nome - [@Dagon67](https://github.com/Dagon67)

Link do Projeto: [https://github.com/Dagon67/treino-mira](https://github.com/Dagon67/treino-mira) 