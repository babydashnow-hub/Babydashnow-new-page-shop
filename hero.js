/* ==========================================================
   BabyDashNow™ Hero — Sticky Mobile CTA
   Shows a fixed bottom CTA once the in-hero button scrolls
   out of view. Mobile only (hidden via CSS on desktop).
   ========================================================== */
(function () {
  'use strict';

  var stickyCta = document.querySelector('.bdn-sticky-cta');
  var heroCta = document.querySelector('.bdn-hero__cta-primary');

  if (!stickyCta || !heroCta) return;

  // Use IntersectionObserver for performance — no scroll listeners.
  if (!('IntersectionObserver' in window)) {
    // Fallback: just never show the sticky bar on very old browsers.
    return;
  }

  var observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          stickyCta.classList.remove('is-visible');
          stickyCta.setAttribute('aria-hidden', 'true');
        } else {
          stickyCta.classList.add('is-visible');
          stickyCta.setAttribute('aria-hidden', 'false');
        }
      });
    },
    { threshold: 0 }
  );

  observer.observe(heroCta);
})();
