// Instalação PWA
let deferredInstallPrompt = null;
const installButton = document.getElementById('installApp');

window.addEventListener('beforeinstallprompt', (event) => {
  event.preventDefault();
  deferredInstallPrompt = event;
  if (installButton) installButton.hidden = false;
});

if (installButton) {
  installButton.addEventListener('click', async () => {
    if (!deferredInstallPrompt) return;

    deferredInstallPrompt.prompt();
    await deferredInstallPrompt.userChoice;
    deferredInstallPrompt = null;
    installButton.hidden = true;
  });
}

window.addEventListener('appinstalled', () => {
  if (installButton) installButton.hidden = true;
});

// Registro do Service Worker
if (
  'serviceWorker' in navigator &&
  (location.protocol === 'https:' || location.hostname === 'localhost')
) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('./sw.js').catch((error) => {
      console.error('Não foi possível registrar o Service Worker:', error);
    });
  });
}
