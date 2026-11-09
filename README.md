# Sportfolio — protótipo PWA

Esta versão acrescenta suporte inicial a Progressive Web App (PWA) ao protótipo HTML existente.

## O que foi adicionado
- `manifest.webmanifest`: nome, ícones, cores e comportamento de instalação.
- `sw.js`: cache do app shell e fallback básico para navegação offline.
- `icons/`: ícones Android/PWA e Apple Touch Icon.
- Metadados para instalação no iOS.
- Botão de instalação quando o navegador oferece `beforeinstallprompt`.
- Registro automático do Service Worker em HTTPS ou localhost.

## Publicar pelo GitHub Pages
1. Extraia o ZIP.
2. Substitua os arquivos correspondentes no repositório pelo conteúdo desta pasta.
3. Mantenha `index.html`, `manifest.webmanifest`, `sw.js` e a pasta `icons/` na raiz do repositório.
4. No GitHub, abra **Settings → Pages** e publique a branch `main`, pasta `/(root)`.
5. Aguarde a publicação e abra a URL HTTPS do GitHub Pages.

## Instalar para testes
- Android (Samsung/Xiaomi): abra o link no Chrome; use **Instalar app** quando aparecer ou o menu do navegador → **Instalar aplicativo / Adicionar à tela inicial**.
- iPhone: abra o link no Safari → **Compartilhar** → **Adicionar à Tela de Início**.

## Limitações desta versão
- É um protótipo front-end com dados fictícios.
- Não há autenticação, banco de dados, sincronização entre dispositivos nem upload real de mídia.
- O cache offline mantém a interface básica disponível, mas não salva alterações de dados.
- No iOS, a instalação é feita pelo menu Compartilhar do Safari; o botão de instalação do navegador não é suportado da mesma forma.
- Após atualizar arquivos, o Service Worker pode levar uma abertura/reabertura para atualizar o cache. Se necessário, remova o app da tela inicial e limpe os dados do site.

## Observação
O nome Sportfolio está mantido como nome de trabalho do repositório. A identidade final pode ser alterada depois.
