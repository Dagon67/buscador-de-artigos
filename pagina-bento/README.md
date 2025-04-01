# Página Bento

Uma landing page moderna e responsiva construída com HTML5, SCSS e JavaScript puro. O projeto utiliza as melhores práticas de desenvolvimento web e oferece uma experiência de usuário fluida e agradável.

## Características

- Design moderno e minimalista
- Totalmente responsivo
- Animações suaves
- Otimizado para performance
- Código limpo e bem organizado
- Sem dependências de frameworks

## Tecnologias Utilizadas

- HTML5
- SCSS (com variáveis, mixins e funções)
- JavaScript ES6+
- Font Awesome para ícones
- Google Fonts

## Estrutura do Projeto

```
pagina-bento/
├── index.html
├── css/
│   ├── style.css
│   └── animations.css
├── scss/
│   ├── style.scss
│   └── animations.scss
├── js/
│   ├── main.js
│   └── animations.js
├── img/
│   ├── logo.svg
│   ├── hero.svg
│   └── about.svg
└── README.md
```

## Recursos

1. **Design Responsivo**
   - Layout adaptativo para todos os dispositivos
   - Mobile-first approach
   - Breakpoints otimizados

2. **Animações**
   - Efeitos de scroll
   - Transições suaves
   - Animações de hover
   - Parallax
   - Contador animado
   - Efeito de digitação

3. **Performance**
   - Carregamento lazy de imagens
   - CSS minificado
   - JavaScript otimizado
   - Imagens otimizadas

4. **Usabilidade**
   - Navegação intuitiva
   - Menu responsivo
   - Scroll suave
   - Formulário de contato funcional
   - Indicador de progresso de scroll

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/Dagon67/pagina-bento.git
cd pagina-bento
```

2. Para desenvolvimento com SCSS:
   - Instale o Sass globalmente:
   ```bash
   npm install -g sass
   ```
   - Compile o SCSS:
   ```bash
   sass scss/style.scss css/style.css --watch
   sass scss/animations.scss css/animations.css --watch
   ```

3. Abra o arquivo `index.html` em seu navegador ou use um servidor local.

## Personalização

### Cores
Edite as variáveis no arquivo `scss/style.scss`:
```scss
$primary-color: #4A90E2;
$secondary-color: #2C3E50;
$accent-color: #E74C3C;
```

### Fontes
Altere as fontes no arquivo `scss/style.scss`:
```scss
body {
    font-family: 'Inter', sans-serif;
}
```

### Animações
Personalize as animações em `scss/animations.scss` e `js/animations.js`.

## Desenvolvimento

1. **Estrutura HTML**
   - Semântica
   - Acessibilidade
   - SEO-friendly

2. **Estilos SCSS**
   - Arquitetura modular
   - Reutilização de código
   - Manutenibilidade

3. **JavaScript**
   - Código modular
   - Event handling
   - Animações performáticas

## Contribuindo

1. Fork o projeto
2. Crie sua Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

## Contato

Seu Nome - [@Dagon67](https://github.com/Dagon67)

Link do Projeto: [https://github.com/Dagon67/pagina-bento](https://github.com/Dagon67/pagina-bento) 