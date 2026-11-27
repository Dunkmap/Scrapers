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

// Article / How-to tabs. Swaps the body panel and the matching 'On this page'
// list, and opens the guide when the URL points at one of its sections.
document.addEventListener('DOMContentLoaded', function () {
  (function () {
      var tabs = [].slice.call(document.querySelectorAll('.tabbar [role="tab"]'));
      if (!tabs.length) return;
      var tocLists = {
        'panel-article': document.querySelector('[data-toc="article"]'),
        'panel-howto': document.querySelector('[data-toc="howto"]')
      };

      function select(tab, opts) {
        opts = opts || {};
        tabs.forEach(function (t) {
          var on = t === tab;
          var panel = document.getElementById(t.getAttribute('aria-controls'));
          t.setAttribute('aria-selected', on ? 'true' : 'false');
          t.tabIndex = on ? 0 : -1;
          if (panel) panel.hidden = !on;
          var list = tocLists[t.getAttribute('aria-controls')];
          if (list) list.hidden = !on;
        });
        if (opts.focus) tab.focus();
        if (opts.scroll) {
          var bar = document.querySelector('.tabbar');
          if (bar) bar.scrollIntoView({ block: 'start', behavior: 'smooth' });
        }
        document.dispatchEvent(new CustomEvent('tabchange'));
      }

      tabs.forEach(function (tab, i) {
        tab.addEventListener('click', function () {
          if (tab.getAttribute('aria-selected') === 'true') return;
          select(tab, { scroll: true });
          var slug = tab.id === 'tb-howto' ? '#how-to-use-it' : '#article';
          if (history.replaceState) history.replaceState(null, '', slug);
        });
        tab.addEventListener('keydown', function (e) {
          var next = null;
          if (e.key === 'ArrowRight') next = tabs[(i + 1) % tabs.length];
          else if (e.key === 'ArrowLeft') next = tabs[(i - 1 + tabs.length) % tabs.length];
          if (!next) return;
          e.preventDefault();
          select(next, { focus: true });
        });
      });

      // A link or a shared URL pointing into the guide opens the guide tab.
      function fromHash() {
        var h = location.hash;
        if (!h || h === '#article') return;
        var inHowto = h === '#how-to-use-it' ||
          (tocLists['panel-howto'] &&
           tocLists['panel-howto'].querySelector('a[href="' + h + '"]'));
        if (!inHowto) return;
        select(document.getElementById('tb-howto'));
        var target = h === '#how-to-use-it' ? null : document.querySelector(h);
        if (target) target.scrollIntoView({ block: 'start' });
      }
      window.addEventListener('hashchange', fromHash);
      fromHash();
    })();
});
