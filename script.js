// Marks the page as JS-enabled before it paints, so .reveal elements start hidden.
document.documentElement.classList.add('js');

document.addEventListener('DOMContentLoaded', () => {
  const io = new IntersectionObserver(entries => entries.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
  }), { threshold: .12 });
  document.querySelectorAll('.reveal').forEach(el => io.observe(el));

  document.querySelectorAll('.card').forEach(card => card.addEventListener('pointermove', e => {
    const r = card.getBoundingClientRect();
    card.style.setProperty('--mx', (e.clientX - r.left) + 'px');
    card.style.setProperty('--my', (e.clientY - r.top) + 'px');
  }));

  // Sends each link click to Google Tag Manager as a "link_click" event, with the
  // card's product name, so GA4 can show which scrapers and extensions get clicked.
  // The same event also goes straight to GA4 through gtag.
  window.dataLayer = window.dataLayer || [];
  document.addEventListener('click', e => {
    const a = e.target.closest('a[href]');
    if (!a) return;
    const card = a.closest('.card');
    const href = a.getAttribute('href');
    const params = {
      link_type: href.includes('apify.com') ? 'apify' : href.includes('chromewebstore') ? 'chrome_store'
        : href.startsWith('mailto:') ? 'email' : href.startsWith('#') ? 'in_page' : 'other',
      item_name: (card?.querySelector('h4, h3') || a).textContent.trim(),
      section: a.closest('section, header, footer, nav')?.id || a.closest('footer, nav')?.tagName.toLowerCase() || '',
      link_url: a.href
    };
    window.dataLayer.push({ event: 'link_click', ...params });
    if (typeof gtag === 'function') gtag('event', 'link_click', params);
  });
});

// Click-to-load YouTube Shorts.
// The page ships only a local poster image; the first press swaps in the
// privacy-enhanced (youtube-nocookie) player, already playing. Nothing
// reaches YouTube before that press.
document.addEventListener('click', e => {
  const btn = e.target.closest('.shortvid-play');
  if (!btn) return;
  const id = btn.dataset.yt;
  if (!id) return;
  const frame = document.createElement('iframe');
  frame.src = 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(id) +
    '?autoplay=1&rel=0&playsinline=1';
  frame.title = btn.getAttribute('aria-label') || 'Video';
  frame.loading = 'lazy';
  frame.allow = 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture; web-share';
  frame.referrerPolicy = 'strict-origin-when-cross-origin';
  frame.allowFullscreen = true;
  btn.replaceWith(frame);
});
