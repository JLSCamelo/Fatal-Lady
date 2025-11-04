(function () {
  // roda após parse do HTML se usar 'defer'
  try {
    document.addEventListener('DOMContentLoaded', () => {
      // --- debug flag ---
      const DEBUG = false;

      // Lê param msg
      const params = new URLSearchParams(window.location.search);
      const msg = params.get('msg');

      if (DEBUG) console.log('[pop_up] query param msg =', msg);

      if (!msg) return; // nada a fazer

      // Mapeia mensagens
      const map = {
        // ⚡ CORREÇÃO: Removido o 'success' daqui.
        invalid: { text: 'Usuário ou senha incorretos.', type: 'error' },
      };

      const payload = map[msg] || null;
      if (!payload) {
        if (DEBUG) console.log('[pop_up] msg desconhecido:', msg);
        // limpa o param mesmo que desconhecido para evitar loop
        params.delete('msg');
        const newUrl = window.location.pathname + (params.toString() ? '?' + params.toString() : '');
        history.replaceState(null, '', newUrl);
        return;
      }

      // --- Injeta estilos e cria container (mantido, fora do snippet por espaço) ---
      // ...

      // --- Lógica de criação do Toast (simplificada para o contexto) ---
      const container = document.getElementById('pop-up-container') || document.body; 

      const node = document.createElement('div');
      // A classe será 'toast error' se msg=invalid (já que success foi removido)
      node.className = 'toast ' + (payload.type === 'success' ? 'success' : 'error'); 

      const text = document.createElement('div');
      text.className = 'text';
      text.textContent = payload.text || '';

      const closeBtn = document.createElement('button');
      closeBtn.className = 'close';
      closeBtn.type = 'button';
      closeBtn.innerText = '✕';
      closeBtn.onclick = () => {
        node.classList.remove('show');
        setTimeout(() => node.remove(), 320);
      };

      node.appendChild(text);
      node.appendChild(closeBtn);
      container.appendChild(node);

      // mostra com anim
      requestAnimationFrame(() => node.classList.add('show'));

      // auto-hide
      const HIDE_MS = 3500;
      setTimeout(() => {
        node.classList.remove('show');
        setTimeout(() => { try { node.remove(); } catch(e){} }, 320);
      }, HIDE_MS);

      // remove msg da url sem recarregar (para não reaparecer)
      try {
        params.delete('msg');
        const newQuery = params.toString();
        const newUrl = window.location.pathname + (newQuery ? '?' + newQuery : '');
        history.replaceState(null, '', newUrl);
        if (DEBUG) console.log('[pop_up] removed msg param');
      } catch (e) {
        if (DEBUG) console.error('[pop_up] Falha ao limpar URL:', e);
      }
    });
  } catch (e) {
    console.error('[pop_up] Erro ao carregar pop-up:', e);
  }
})();