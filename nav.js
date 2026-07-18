/**
 * Huaxing PCBA — Shared Navigation Injection
 * Injects consistent dropdown Industries nav into all pages.
 */
(function(){
  var nav = document.getElementById('navLinks');
  if (!nav) return;

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
      '<span class="nav-dropdown-trigger">Industries <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:12px;height:12px"><polyline points="6 9 12 15 18 9"/></svg></span>' +
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

  // Dropdown toggle logic
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
