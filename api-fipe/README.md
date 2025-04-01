# Consulta FIPE

Interface web para consulta de preços de veículos utilizando a API FIPE (Fundação Instituto de Pesquisas Econômicas).

## Recursos

- Consulta de preços de veículos
- Seleção dinâmica de:
  - Tipo de veículo (carro, moto, caminhão)
  - Marca
  - Modelo
  - Ano
- Exibição detalhada de informações:
  - Preço médio
  - Código FIPE
  - Combustível
  - Mês/ano de referência
- Interface responsiva
- Histórico de consultas
- Exportação de resultados

## Tecnologias

- HTML5
- CSS3
- JavaScript (ES6+)
- Bootstrap 5
- API FIPE
- LocalStorage para histórico
- Chart.js para gráficos

## Funcionalidades

- Consulta em tempo real
- Validação de dados
- Cache de resultados
- Histórico de pesquisas
- Comparação de preços
- Gráficos de variação
- Exportação para CSV/PDF

## Como Usar

1. Clone o repositório:
```bash
git clone https://github.com/Dagon67/api-fipe.git
cd api-fipe
```

2. Abra o arquivo `index.html` em seu navegador.

3. Selecione sequencialmente:
   - Tipo de veículo
   - Marca
   - Modelo
   - Ano

4. Visualize os resultados detalhados.

## Estrutura do Projeto

```
api-fipe/
├── index.html
├── css/
│   ├── style.css
│   └── responsive.css
├── js/
│   ├── main.js
│   ├── api.js
│   └── utils.js
├── assets/
│   └── images/
└── README.md
```

## API

O projeto utiliza a API FIPE pública disponível em:
`https://deividfortuna.github.io/fipe/`

### Endpoints Principais

1. Marcas:
```
GET /carros/marcas
GET /motos/marcas
GET /caminhoes/marcas
```

2. Modelos:
```
GET /{tipo}/marcas/{marca}/modelos
```

3. Anos:
```
GET /{tipo}/marcas/{marca}/modelos/{modelo}/anos
```

4. Valor:
```
GET /{tipo}/marcas/{marca}/modelos/{modelo}/anos/{ano}
```

## Personalização

### Estilos
Modifique `css/style.css` para personalizar a aparência:
```css
:root {
  --primary-color: #your-color;
  --secondary-color: #your-color;
  /* ... outras variáveis ... */
}
```

### Configurações
Ajuste parâmetros em `js/config.js`:
```javascript
const CONFIG = {
  cacheTimeout: 3600, // segundos
  maxHistoryItems: 50,
  // ... outras configurações ...
};
```

## Recursos Adicionais

- Exportação de dados em CSV
- Gráficos de variação de preços
- Histórico de consultas
- Comparador de veículos
- Favoritos
- Notificações de alterações

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

Link do Projeto: [https://github.com/Dagon67/api-fipe](https://github.com/Dagon67/api-fipe) 