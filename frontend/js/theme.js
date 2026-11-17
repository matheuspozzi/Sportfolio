// Aparência: salva a preferência e aplica o tema escolhido.
const themeSelect = document.getElementById('themeSelect');
const themeHelp = document.getElementById('themeHelp');
const themeColorMeta = document.querySelector('meta[name="theme-color"]');

function applyTheme(theme) {
  const validTheme = ['auto', 'light', 'dark'].includes(theme) ? theme : 'auto';
  document.documentElement.setAttribute('data-theme', validTheme);

  if (themeSelect) themeSelect.value = validTheme;

  if (themeHelp) {
    themeHelp.textContent = validTheme === 'auto'
      ? 'O tema acompanha automaticamente a aparência configurada no seu dispositivo.'
      : validTheme === 'light'
        ? 'O Sportfolio utilizará sempre o tema claro neste dispositivo.'
        : 'O Sportfolio utilizará sempre o tema escuro neste dispositivo.';
  }

  const prefersLight = window.matchMedia &&
    window.matchMedia('(prefers-color-scheme: light)').matches;

  const effectiveTheme = validTheme === 'auto'
    ? (prefersLight ? 'light' : 'dark')
    : validTheme;

  if (themeColorMeta) {
    themeColorMeta.setAttribute('content', effectiveTheme === 'light' ? '#f3f6f4' : '#0b1014');
  }
}

let currentTheme = 'auto';

try {
  currentTheme = localStorage.getItem('sportfolio-theme') || 'auto';
} catch (error) {
  currentTheme = 'auto';
}

applyTheme(currentTheme);

if (themeSelect) {
  themeSelect.addEventListener('change', () => {
    const selectedTheme = themeSelect.value;

    try {
      localStorage.setItem('sportfolio-theme', selectedTheme);
    } catch (error) {
      console.warn('Não foi possível salvar a preferência de tema:', error);
    }

    applyTheme(selectedTheme);
  });
}

// Quando estiver em automático, acompanha mudanças na aparência do dispositivo.
const colorSchemeQuery = window.matchMedia('(prefers-color-scheme: light)');

if (colorSchemeQuery.addEventListener) {
  colorSchemeQuery.addEventListener('change', () => {
    const savedTheme = document.documentElement.getAttribute('data-theme') || 'auto';
    if (savedTheme === 'auto') applyTheme('auto');
  });
}
