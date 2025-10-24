// static/js/pop_up.js
// Autonomo: detecta ?msg=success ou ?msg=invalid e mostra toast.
// Coloque <script src="/static/js/pop_up.js" defer></script> antes de </body>

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
        success: { text: 'Login feito com sucesso.', type: 'success' },
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

      // --- injeta estilos uma vez ---
      if (!document.getElementById('pop-up-toast-styles')) {
        const style = document.createElement('style');
        style.id = 'pop-up-toast-styles';
        style.textContent = `
#app-toast { position: fixed; right: 20px; top: 20px; z-index: 9999; display:flex; flex-direction: column; gap:10px; pointer-events: none; }
.toast { pointer-events: auto; min-width: 260px; max-width: 420px; padding: 12px 16px; border-radius: 10px; box-shadow: 0 8px 24px rgba(0,0,0,0.12); color: #fff; font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial; font-size: 14px; opacity: 0; transform: translateY(-8px); transition: opacity 300ms ease, transform 300ms ease; display:flex; align-items:center; justify-content:space-between; gap:12px; }
.toast.show { opacity: 1; transform: translateY(0); }
.toast.success { background: linear-gradient(180deg,#22c55e,#16a34a); }
.toast.error   { background: linear-gradient(180deg,#fb7185,#ef4444); }
.toast .text { flex:1; padding-right:8px; line-height:1.2; }
.toast .close { background: transparent; border: none; color: rgba(255,255,255,0.95); font-weight:700; cursor: pointer; padding:4px; margin-left:8px; font-size: 16px; }
@media (max-width:420px) { #app-toast { left: 12px; right: 12px; top: 12px; } .toast { max-width: 100%; } }
        `;
        document.head.appendChild(style);
      }

      // --- garante container ---
      let container = document.getElementById('app-toast');
      if (!container) {
        container = document.createElement('div');
        container.id = 'app-toast';
        document.body.appendChild(container);
      }

      // cria toast
      const node = document.createElement('div');
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
        if (DEBUG) console.log('[pop_up] removed msg param; newUrl=', newUrl);
      } catch (e) {
        if (DEBUG) console.error('[pop_up] could not remove param', e);
      }
    });
  } catch (err) {
    // nunca quebra o app
    console.error('pop_up.js error:', err);
  }
})();
