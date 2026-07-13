/* Scroll-triggered reveal animations — forEach observer pattern with immediate check */
(function(){
  const revealEls = document.querySelectorAll('.reveal');
  if (!revealEls.length) return;
  const obs = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        obs.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px 0px 0px' });
  revealEls.forEach(el => {
    obs.observe(el);
    // Immediately check if already in viewport (handles race condition)
    const rect = el.getBoundingClientRect();
    if (rect.top < window.innerHeight && rect.bottom > 0) {
      el.classList.add('visible');
      obs.unobserve(el);
    }
  });
  // Fallback: after 1.5s, reveal any still-hidden elements
  setTimeout(() => {
    document.querySelectorAll('.reveal:not(.visible)').forEach(el => {
      el.classList.add('visible');
    });
  }, 1500);
})();
