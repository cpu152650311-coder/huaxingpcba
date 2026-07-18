/**
 * Huaxing PCBA — Shared Navigation Injection
 * Injects nav HTML + critical CSS so the nav works even if
 * design-tokens.css is cached stale or loads slowly from CDN.
 */
(function(){
  var nav = document.getElementById('navLinks');
  if (!nav) return;

  // 1. Inject critical nav CSS — guarantees the nav never breaks
  var style = document.createElement('style');
  style.textContent =
    /* Desktop nav layout */
    '.nav-links{display:flex;gap:40px;align-items:center}' +
    '.nav-links a{' +
      'font-size:14px;font-weight:300;letter-spacing:0.03em;' +
      'color:#b0b0b8;text-decoration:none;transition:color .2s;' +
      'position:relative;white-space:nowrap' +
    '}' +
    '.nav-links a:hover,.nav-links a.active{color:#e8e8ec}' +
    '.nav-links a::after{' +
      'content:"";position:absolute;bottom:-4px;left:0;right:0;' +
      'height:1px;background:#c8963e;transform:scaleX(0);' +
      'transition:transform .25s' +
    '}' +
    '.nav-links a:hover::after,.nav-links a.active::after{transform:scaleX(1)}' +
    /* CTA button */
    '.nav-cta{' +
      'padding:8px 20px;background:rgba(200,150,62,.12);' +
      'border:1px solid rgba(200,150,62,.3);border-radius:4px;' +
      'color:#d4a843!important;font-weight:400' +
    '}' +
    '.nav-cta::after{display:none!important}' +
    '.nav-cta:hover{background:#d4a843;color:#0a0a0b!important}' +
    /* Dropdown container */
    '.nav-dropdown{position:relative;display:inline-flex}' +
    '.nav-dropdown-trigger{' +
      'display:flex;align-items:center;gap:4px;' +
      'font-size:14px;font-weight:300;letter-spacing:0.03em;' +
      'color:#b0b0b8;cursor:pointer;white-space:nowrap' +
    '}' +
    '.nav-dropdown:hover>.nav-dropdown-trigger{color:#e8e8ec}' +
    '.nav-dropdown-trigger svg{width:12px;height:12px;transition:transform .25s}' +
    '.nav-dropdown:hover>.nav-dropdown-trigger svg{transform:rotate(180deg)}' +
    /* Dropdown panel — HIDDEN by default (this is the critical fix) */
    '.nav-dropdown-panel{' +
      'position:absolute;top:100%;left:50%;' +
      'transform:translateX(-50%) translateY(8px);' +
      'background:#16161d;border:1px solid #252530;' +
      'border-radius:8px;padding:8px;min-width:220px;' +
      'opacity:0;visibility:hidden;' +
      'transition:opacity .25s,visibility .25s,transform .25s;' +
      'box-shadow:0 20px 48px rgba(0,0,0,.5);z-index:100' +
    '}' +
    '.nav-dropdown:hover>.nav-dropdown-panel,' +
    '.nav-dropdown.open>.nav-dropdown-panel{' +
      'opacity:1;visibility:visible;transform:translateX(-50%) translateY(4px)' +
    '}' +
    '.nav-dropdown-panel a{' +
      'display:flex;align-items:center;gap:8px;' +
      'padding:8px 16px;color:#9898a8;font-size:14px;' +
      'border-radius:6px;transition:color .2s,background .2s;' +
      'text-decoration:none;white-space:nowrap' +
    '}' +
    '.nav-dropdown-panel a:hover{color:#d4a843;background:rgba(200,150,62,.08)}' +
    '.nav-dropdown-panel a .dd-icon{' +
      'width:6px;height:6px;border-radius:50%;' +
      'background:#c8963e;flex-shrink:0;opacity:.6' +
    '}' +
    /* Mobile responsive */
    '@media(max-width:1024px){' +
      '.nav-links{display:none;flex-direction:column;' +
        'position:absolute;top:100%;left:0;right:0;' +
        'background:#0d0d14;border-top:1px solid #1a1a25;' +
        'padding:16px 24px;gap:0;z-index:99' +
      '}' +
      '.nav-links.mobile-open{display:flex}' +
      '.nav-links a,.nav-dropdown-trigger{' +
        'padding:12px 0;border-bottom:1px solid #1a1a25;font-size:16px' +
      '}' +
      '.nav-cta{margin-top:8px;text-align:center}' +
      '.nav-dropdown{display:flex;flex-direction:column}' +
      '.nav-dropdown-panel{' +
        'position:static;transform:none;opacity:1;visibility:visible;' +
        'background:transparent;border:none;box-shadow:none;' +
        'padding:0 0 0 24px;min-width:0' +
      '}' +
      '.nav-dropdown-panel a{padding:10px 0;font-size:14px;color:#b0b0b8}' +
      '.nav-dropdown-trigger svg{display:none}' +
      '.nav-dropdown:hover>.nav-dropdown-trigger svg{transform:none}' +
      '.nav-dropdown:hover>.nav-dropdown-panel{transform:none}' +
    '}';
  document.head.appendChild(style);

  // 2. Inject nav HTML
  var path = location.pathname;
  function active(p) {
    if (p === '/' && (path === '/' || path === '/index.html')) return ' class="active"';
    if (p !== '/' && path.startsWith(p)) return ' class="active"';
    return '';
  }

  nav.innerHTML =
    '<a href="/"' + active('/') + '>Home</a>' +
    '<a href="/capabilities/"' + active('/capabilities/') + '>Capabilities</a>' +
    '<div class="nav-dropdown" id="industriesDropdown">' +
      '<span class="nav-dropdown-trigger">Industries <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg></span>' +
      '<div class="nav-dropdown-panel">' +
        '<a href="/industries/automotive/"><span class="dd-icon"></span>Automotive</a>' +
        '<a href="/industries/medical/"><span class="dd-icon"></span>Medical</a>' +
        '<a href="/industries/industrial/"><span class="dd-icon"></span>Industrial</a>' +
        '<a href="/industries/iot/"><span class="dd-icon"></span>IoT</a>' +
        '<a href="/industries/telecom/"><span class="dd-icon"></span>Telecom &amp; 5G</a>' +
        '<a href="/industries/energy/"><span class="dd-icon"></span>New Energy</a>' +
        '<a href="/industries/consumer/"><span class="dd-icon"></span>Consumer</a>' +
      '</div>' +
    '</div>' +
    '<a href="/quote/"' + active('/quote/') + '>Quick Quote</a>' +
    '<a href="/about/"' + active('/about/') + '>About</a>' +
    '<a href="/contact/"' + active('/contact/') + '>Contact</a>' +
    '<a href="/blog/"' + active('/blog/') + '>Blog</a>' +
    '<a href="#inquiry" class="nav-cta" onclick="if(typeof openModal==\'function\')openModal();return false">Get Quote</a>';

  // 3. Dropdown toggle (click to open/close on mobile + desktop)
  var dd = document.getElementById('industriesDropdown');
  if (dd) {
    document.addEventListener('click', function(e) {
      if (!dd.contains(e.target)) dd.classList.remove('open');
    });
    dd.querySelector('.nav-dropdown-trigger').addEventListener('click', function(e) {
      e.preventDefault();
      dd.classList.toggle('open');
    });
  }
})();
