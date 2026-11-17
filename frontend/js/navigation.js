const labels = {
  overview: 'Visão geral',
  profile: 'Meu perfil',
  career: 'Histórico esportivo',
  physical: 'Evolução física',
  matches: 'Partidas e estatísticas',
  media: 'Fotos e vídeos',
  privacy: 'Privacidade',
  settings: 'Configurações'
};

const guidance = {
  overview: {
    title: 'Comece por aqui',
    body: 'A visão geral reúne os principais números e acontecimentos da sua trajetória. Use os atalhos para acessar uma área ou o botão “Novo registro” para escolher o que deseja atualizar.',
    tip: 'Dica: você pode preencher seu histórico aos poucos. Não é necessário completar tudo de uma vez.'
  },
  profile: {
    title: 'Organize sua identidade esportiva',
    body: 'Mantenha seus dados, modalidade, posição e apresentação atualizados. Essas informações ajudam outras pessoas a entenderem quem você é como atleta.',
    tip: 'Dica: comece pelos dados principais e complemente a apresentação quando quiser.'
  },
  career: {
    title: 'Registre cada etapa da sua trajetória',
    body: 'Adicione uma passagem para cada período em um clube. Se voltou ao mesmo clube em outra temporada, registre uma nova passagem para preservar a história corretamente.',
    tip: 'Dica: inclua categoria e período. Depois você pode complementar com competições, conquistas e evidências.'
  },
  physical: {
    title: 'Acompanhe sua evolução ao longo do tempo',
    body: 'Cada avaliação deve ter uma data. Registre medidas e testes com suas unidades e observações para conseguir comparar resultados de forma coerente.',
    tip: 'Dica: quando possível, mantenha o mesmo método de avaliação para comparar resultados.'
  },
  matches: {
    title: 'Registre somente partidas em que participou',
    body: 'Cadastre os dados da partida e depois informe sua participação, minutos e estatísticas. Diferencie um resultado zero de uma informação que ainda não foi registrada.',
    tip: 'Dica: você pode adicionar detalhes de desempenho e mídia depois de registrar os dados principais.'
  },
  media: {
    title: 'Guarde os momentos da sua carreira',
    body: 'Organize fotos e vídeos por clube, temporada, partida ou categoria. Assim fica mais fácil encontrar um registro no futuro.',
    tip: 'Dica: use títulos e descrições que ajudem a identificar o contexto de cada arquivo.'
  },
  privacy: {
    title: 'Você controla o que compartilha',
    body: 'Revise a visibilidade do perfil e de cada tipo de informação antes de compartilhar sua trajetória.',
    tip: 'Dica: informações privadas continuam disponíveis para você; compartilhar é uma escolha.'
  },
  settings: {
    title: 'Ajuste sua experiência',
    body: 'Esta área reunirá preferências da conta e opções de personalização conforme o produto evoluir.',
    tip: 'Dica: as configurações de privacidade ficam na seção “Privacidade”.'
  }
};

const sidebar = document.getElementById('sidebar');

const mobileOverlay = document.createElement('div');
mobileOverlay.className = 'mobile-overlay';
mobileOverlay.setAttribute('aria-hidden', 'true');
document.body.appendChild(mobileOverlay);

function closeMobileMenu() {
  sidebar.classList.remove('open');
  mobileOverlay.classList.remove('show');
  document.getElementById('menu').setAttribute('aria-expanded', 'false');
}

function go(id) {
  if (!labels[id]) return;

  document.querySelectorAll('.section').forEach(section => {
    section.classList.toggle('active', section.id === id);
  });

  document.querySelectorAll('.nav button[data-page]').forEach(button => {
    const active = button.dataset.page === id;
    button.classList.toggle('active', active);

    if (active) button.setAttribute('aria-current', 'page');
    else button.removeAttribute('aria-current');
  });

  document.getElementById('crumb').textContent = labels[id];
  closeMobileMenu();

  if (location.hash !== '#' + id) {
    history.replaceState(null, '', '#' + id);
  }

  window.scrollTo({
    top: 0,
    behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'
  });
}

document.querySelectorAll('.nav button[data-page]').forEach(button => {
  button.addEventListener('click', () => go(button.dataset.page));
});

document.querySelectorAll('[data-goto]').forEach(button => {
  button.addEventListener('click', () => go(button.dataset.goto));
});

document.getElementById('menu').addEventListener('click', () => {
  const open = !sidebar.classList.contains('open');
  sidebar.classList.toggle('open', open);
  mobileOverlay.classList.toggle('show', open);
  document.getElementById('menu').setAttribute('aria-expanded', String(open));
});

mobileOverlay.addEventListener('click', closeMobileMenu);

// Ajuda contextual
document.querySelectorAll('.section').forEach(section => {
  const data = guidance[section.id];
  const head = section.querySelector('.pagehead');
  if (!data || !head) return;

  const wrap = document.createElement('div');
  wrap.className = 'page-help';

  const button = document.createElement('button');
  button.className = 'help-toggle';
  button.type = 'button';
  button.setAttribute('aria-expanded', 'false');
  button.innerHTML = '<span aria-hidden="true">ⓘ</span> Como funciona esta área?';

  const panel = document.createElement('div');
  panel.className = 'help-panel';
  panel.innerHTML = `<strong>${data.title}</strong><p>${data.body}</p><span class="help-tip">${data.tip}</span>`;

  button.addEventListener('click', () => {
    const open = panel.classList.toggle('open');
    button.setAttribute('aria-expanded', String(open));
    button.innerHTML = `<span aria-hidden="true">ⓘ</span> ${open ? 'Ocultar orientação' : 'Como funciona esta área?'}`;
  });

  wrap.append(button, panel);
  head.insertAdjacentElement('afterend', wrap);
});

// Busca na navegação
const navSearch = document.getElementById('navSearch');
const navSearchEmpty = document.getElementById('navSearchEmpty');

navSearch.addEventListener('input', () => {
  const term = navSearch.value.trim().toLocaleLowerCase('pt-BR');
  let visible = 0;

  document.querySelectorAll('.nav button[data-page]').forEach(button => {
    const match = button.textContent.toLocaleLowerCase('pt-BR').includes(term);
    button.hidden = !match;
    if (match) visible++;
  });

  document.querySelectorAll('.navlabel').forEach(label => {
    const nav = label.nextElementSibling;
    label.hidden = !!term && !Array.from(nav.querySelectorAll('button')).some(button => !button.hidden);
  });

  navSearchEmpty.hidden = visible !== 0;
});

document.addEventListener('keydown', event => {
  if (
    event.key === '/' &&
    !['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName) &&
    !event.ctrlKey &&
    !event.metaKey
  ) {
    event.preventDefault();
    navSearch.focus();
  }

  if (event.key === 'Escape') {
    closeMobileMenu();
    if (quickDialog.open) quickDialog.close();
  }
});

// Ações rápidas
const quickDialog = document.getElementById('quickDialog');

document.getElementById('openQuickActions').addEventListener('click', () => quickDialog.showModal());
document.getElementById('closeQuickActions').addEventListener('click', () => quickDialog.close());

document.querySelectorAll('[data-quick-goto]').forEach(button => {
  button.addEventListener('click', () => {
    const target = button.dataset.quickGoto;
    quickDialog.close();
    go(target);
  });
});
