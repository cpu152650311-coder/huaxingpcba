/**
 * Huaxing PCBA — Shared Navigation Injection
 * Injects nav HTML + critical CSS so the nav works even if
 * design-tokens.css is cached stale or loads slowly from CDN.
 */
(function(){
  var nav = document.getElementById('navLinks');
  if (!nav) return;

  // 1. Inject critical nav CSS
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
    /* Dropdown panel */
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
      'display:flex;align-items:center;gap:10px;' +
      'padding:8px 14px;color:#b0b0b8;font-size:14px;' +
      'border-radius:6px;transition:color .2s,background .2s;' +
      'text-decoration:none;white-space:nowrap' +
    '}' +
    '.nav-dropdown-panel a:hover{color:#e8e8ec;background:rgba(200,150,62,.08)}' +
    /* Flyout trigger — "PCB Types" with right-arrow */
    '.nav-flyout-trigger{' +
      'position:relative;' +
      'display:flex!important;align-items:center!important;' +
      'justify-content:space-between!important;' +
      'padding:8px 14px!important;' +
      'color:#b0b0b8!important;font-size:14px!important;' +
      'border-radius:6px!important;cursor:pointer!important;' +
      'transition:color .2s,background .2s!important;' +
      'white-space:nowrap!important;text-decoration:none!important' +
    '}' +
    '.nav-flyout-trigger:hover{color:#e8e8ec!important;background:rgba(200,150,62,.08)!important}' +
    '.nav-flyout-trigger>a{color:inherit!important;text-decoration:none!important;flex:1}' +
    '.nav-flyout-trigger .ft-arrow{width:12px;height:12px;flex-shrink:0;color:#666}' +
    '.nav-flyout-trigger:hover .ft-arrow{color:#c8963e}' +
    /* Flyout sub-panel — slides out to the RIGHT */
    '.nav-flyout-panel{' +
      'position:absolute;left:calc(100% + 4px);top:-8px;' +
      'background:#16161d;border:1px solid #252530;' +
      'border-radius:8px;padding:8px;min-width:240px;' +
      'opacity:0;visibility:hidden;pointer-events:none;' +
      'transition:opacity .2s,visibility .2s;' +
      'box-shadow:0 20px 48px rgba(0,0,0,.5);z-index:101' +
    '}' +
    '.nav-flyout-trigger:hover>.nav-flyout-panel{' +
      'opacity:1;visibility:visible;pointer-events:auto' +
    '}' +
    '.nav-flyout-panel a{' +
      'display:flex!important;align-items:center!important;' +
      'gap:10px!important;' +
      'padding:7px 14px!important;color:#b0b0b8!important;' +
      'font-size:13px!important;border-radius:6px!important;' +
      'transition:color .2s,background .2s!important;' +
      'text-decoration:none!important;white-space:nowrap!important' +
    '}' +
    '.nav-flyout-panel a:hover{color:#e8e8ec!important;background:rgba(200,150,62,.08)!important}' +
    /* Fade-in with slight shift for flyout panel */
    '@keyframes flyoutIn{from{opacity:0;transform:translateX(-4px)}to{opacity:1;transform:translateX(0)}}' +
    '.nav-flyout-trigger:hover>.nav-flyout-panel{animation:flyoutIn .2s ease}' +
    /* ── Mobile ≤768px: fullscreen overlay (matches design-tokens.css) ── */
    '@media(max-width:768px){' +
      '.nav-links{display:none}' +
      '.nav-links.mobile-open{' +
        'display:flex;flex-direction:column;' +
        'position:fixed;top:0;left:0;right:0;bottom:0;' +
        'background:#08080b;' +
        'padding:calc(72px + 24px) 16px 16px;' +
        'gap:0;z-index:200;overflow-y:auto' +
      '}' +
      '.nav-links a,.nav-dropdown-trigger{' +
        'padding:13px 0;border-bottom:1px solid #252530;font-size:16px;color:#e8e8ec' +
      '}' +
      '.nav-cta{margin-top:12px;text-align:center;border-bottom:none!important}' +
      '.nav-dropdown{display:flex;flex-direction:column}' +
      '.nav-dropdown-panel{' +
        'position:static;transform:none;opacity:1;visibility:visible;' +
        'background:transparent;border:none;box-shadow:none;' +
        'padding:0 0 0 20px;min-width:0' +
      '}' +
      '.nav-dropdown-panel a{padding:10px 0;font-size:14px;color:#b0b0b8}' +
      '.nav-dropdown-trigger svg{display:none}' +
      '.nav-dropdown:hover>.nav-dropdown-trigger svg{transform:none}' +
      '.nav-dropdown:hover>.nav-dropdown-panel{transform:none}' +
      '.nav-flyout-trigger{flex-wrap:wrap!important}' +
      '.nav-flyout-panel{' +
        'position:static!important;opacity:1!important;visibility:visible!important;' +
        'pointer-events:auto!important;' +
        'background:transparent!important;border:none!important;' +
        'box-shadow:none!important;padding:0 0 0 16px!important;' +
        'min-width:0!important;animation:none!important;display:none!important' +
      '}' +
      '.nav-flyout-trigger.open>.nav-flyout-panel{display:block!important}' +
      '.nav-flyout-trigger .ft-arrow{display:none}' +
    '}' +
    /* ── Tablet 769-1024px: dropdown overlay ── */
    '@media(min-width:769px) and (max-width:1024px){' +
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
      '.nav-flyout-trigger{flex-wrap:wrap!important}' +
      '.nav-flyout-panel{' +
        'position:static!important;opacity:1!important;visibility:visible!important;' +
        'pointer-events:auto!important;' +
        'background:transparent!important;border:none!important;' +
        'box-shadow:none!important;padding:0 0 0 16px!important;' +
        'min-width:0!important;animation:none!important;display:none!important' +
      '}' +
      '.nav-flyout-trigger.open>.nav-flyout-panel{display:block!important}' +
      '.nav-flyout-trigger .ft-arrow{display:none}' +
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
    '<div class="nav-dropdown" id="capabilitiesDropdown">' +
      '<span class="nav-dropdown-trigger">Capabilities <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg></span>' +
      '<div class="nav-dropdown-panel">' +
        /* PCB Types — flyout trigger */
        '<span class="nav-flyout-trigger" id="pcbTypesFlyout">' +
          '<a href="/capabilities/pcb-types/">PCB Types</a>' +
          '<svg class="ft-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 6 15 12 9 18"/></svg>' +
          '<div class="nav-flyout-panel">' +
            '<a href="/capabilities/pcb-types/hdi/">HDI · Any-Layer</a>' +
            '<a href="/capabilities/pcb-types/flex/">Flex · Polyimide</a>' +
            '<a href="/capabilities/pcb-types/rigid-flex/">Rigid-Flex · Hybrid</a>' +
            '<a href="/capabilities/pcb-types/rf/">RF / Microwave · Rogers</a>' +
            '<a href="/capabilities/pcb-types/high-speed/">High-Speed · 112Gbps</a>' +
            '<a href="/capabilities/pcb-types/heavy-copper/">Heavy Copper · 12oz</a>' +
            '<a href="/capabilities/pcb-types/aluminum/">Aluminum MCPCB</a>' +
            '<a href="/capabilities/pcb-types/ceramic/">Ceramic · Al₂O₃ / AlN</a>' +
          '</div>' +
        '</span>' +
        '<a href="/capabilities/advanced-pcb/">Advanced PCB</a>' +
        '<a href="/capabilities/pcb-fabrication/">PCB Fabrication</a>' +
        '<a href="/capabilities/pcba-assembly/">PCBA Assembly</a>' +
        '<a href="/capabilities/components-sourcing/">Components Sourcing</a>' +
      '</div>' +
    '</div>' +
    '<div class="nav-dropdown" id="industriesDropdown">' +
      '<span class="nav-dropdown-trigger">Industries <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg></span>' +
      '<div class="nav-dropdown-panel">' +
        '<a href="/industries/automotive/">Automotive</a>' +
        '<a href="/industries/medical/">Medical</a>' +
        '<a href="/industries/industrial/">Industrial</a>' +
        '<a href="/industries/iot/">IoT</a>' +
        '<a href="/industries/telecom/">Telecom &amp; 5G</a>' +
        '<a href="/industries/energy/">New Energy</a>' +
        '<a href="/industries/consumer/">Consumer</a>' +
        '<a href="/industries/aerospace/">Aerospace &amp; Defense</a>' +
      '</div>' +
    '</div>' +
    '<a href="/quote/"' + active('/quote/') + '>Quick Quote</a>' +
    '<a href="/about/"' + active('/about/') + '>About</a>' +
    '<a href="/contact/"' + active('/contact/') + '>Contact</a>' +
    '<a href="/blog/"' + active('/blog/') + '>Blog</a>' +
    '<a href="#inquiry" class="nav-cta" onclick="if(typeof openModal==\'function\')openModal();return false">Get Quote</a>';

  // 3. Dropdown toggles (click to open/close)
  document.addEventListener('click', function(e) {
    // Close all dropdowns on outside click
    ['capabilitiesDropdown','industriesDropdown'].forEach(function(id) {
      var dd = document.getElementById(id);
      if (dd && !dd.contains(e.target)) dd.classList.remove('open');
    });
    // Close flyout on outside click
    var flyout = document.getElementById('pcbTypesFlyout');
    if (flyout && !flyout.contains(e.target)) flyout.classList.remove('open');
  });

  // Dropdown click toggles (for mobile / tap devices)
  ['capabilitiesDropdown','industriesDropdown'].forEach(function(id) {
    var dd = document.getElementById(id);
    if (!dd) return;
    var trigger = dd.querySelector('.nav-dropdown-trigger');
    if (trigger) {
      trigger.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        dd.classList.toggle('open');
      });
    }
  });

  // Flyout click toggle for mobile
  var flyout = document.getElementById('pcbTypesFlyout');
  if (flyout) {
    flyout.addEventListener('click', function(e) {
      if (window.innerWidth <= 1024) {
        e.preventDefault();
        e.stopPropagation();
        flyout.classList.toggle('open');
      }
    });
  }
})();
